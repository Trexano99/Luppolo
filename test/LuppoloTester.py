import os

from antlr4 import InputStream, CommonTokenStream

from src.grammar.LuppoloGrammar import LuppoloGrammar
from src.ast.AstGenerator import AstGenerator


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
        resultOfTest += f"Not passed tests: {str(len(notPassed:=[key for key in result if not result[key]])) }\{len(result)} \n"
        for key in notPassed:
            resultOfTest += f"Test {key} failed\n"
        resultOfTest += f"Passed tests: {str(len([key for key in result if result[key]]))}\{len(result)}\n"

        print(resultOfTest)

    @staticmethod
    def __executeGrammarTest(filepath):
        fileContent = open(filepath, 'r').read()
        lexer = LuppoloGrammar.luppoloLexer(InputStream(fileContent))
        parser = LuppoloGrammar.luppoloParser(CommonTokenStream(lexer))
        try:
            AstGenerator().visit(parser.program())
            return True
        except:
            return False