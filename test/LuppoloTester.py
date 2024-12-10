import os

from antlr4 import InputStream, CommonTokenStream

from src.grammar.LuppoloGrammar import LuppoloGrammar
from src.interpreter.interpreter import LuppoloInterpreter
from src.interpreter.LuppoloInterpException import LuppoloInterpException
from src.ast.AstGenerator import AstGenerator
from src.expression.leaf import Rational
from src.utils.LuppoloLogger import LuppoloLogger


class LuppoloTester():

    @staticmethod
    def testGrammar(testValid = True, testErroneous = True):
        grammarTestDir = ".\\test\\grammar"
        result = {}
        if testValid:
            for path, _, files in os.walk(grammarTestDir+"\\valid"):
                for name in files:
                    result[name] = LuppoloTester.__executeGrammarTest(name:=os.path.join(path, name))
        if testErroneous:
            for path, _, files in os.walk(grammarTestDir+"\\erroneous"):
                for name in files:
                    result[name] = not LuppoloTester.__executeGrammarTest(name:=os.path.join(path, name))

        resultOfTest = "RESULT OF GRAMMAR TESTS\n"
        resultOfTest += f"Passed tests: {str(len([key for key in result if result[key]]))}\{len(result)}\n"
        resultOfTest += f"Not passed tests: {str(len(notPassed:=[key for key in result if not result[key]])) }\{len(result)} \n"
        for key in notPassed:
            resultOfTest += f"Test {key} failed\n"

        print(resultOfTest)

    @staticmethod
    def testInterpreter(testValid = True, testErroneous = True):
        interpreterTestDir = ".\\test\\interpreter"
        result = {}
        if testValid:
            for path, _, files in os.walk(interpreterTestDir+"\\valid"):
                for name in files:
                    result[name] = LuppoloTester.__executeInterpreterTest(name:=os.path.join(path, name))
        if testErroneous:
            for path, _, files in os.walk(interpreterTestDir+"\\erroneous"):
                for name in files:
                    result[name] = not LuppoloTester.__executeInterpreterTest(name:=os.path.join(path, name))

        resultOfTest = "RESULT OF INTERPRETER TESTS\n"
        resultOfTest += f"Passed tests: {str(len([key for key in result if result[key]]))}\{len(result)}\n"
        resultOfTest += f"Not passed tests: {str(len(notPassed:=[key for key in result if not result[key]])) }\{len(result)} \n"
        for key in notPassed:
            resultOfTest += f"Test {key} failed\n"

        print(resultOfTest)

        
    def suppressLogger(method):
        def wrapper(self, *args, **kwargs):
            LuppoloLogger.getLogger().disabled = True
            res = method(self, *args, **kwargs)
            LuppoloLogger.getLogger().disabled = False
            return res
        return wrapper
    

    @staticmethod
    @suppressLogger
    def __executeGrammarTest(filepath):
        fileContent = open(filepath, 'r').read()
        lexer = LuppoloGrammar.getLuppoloLexer(fileContent)
        parser = LuppoloGrammar.getLuppoloParser(lexer)
        try:
            AstGenerator().visit(parser.program())
            return True
        except:
            return False
    
    @staticmethod
    @suppressLogger
    def __executeInterpreterTest(filepath):
        fileContent = open(filepath, 'r').read()
        lexer = LuppoloGrammar.getLuppoloLexer(fileContent)
        parser = LuppoloGrammar.getLuppoloParser(lexer)
        astParsedTree = AstGenerator().visit(parser.program())

        try:
            interpreter = LuppoloInterpreter(astParsedTree.children)
            return interpreter.interpretFunc() == Rational(1)
        except Exception as e:
            return False