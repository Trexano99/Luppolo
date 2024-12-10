import argparse, os

from antlr4.tree.Trees import Trees

from src.utils.LuppoloLogger import LuppoloLogger
from src.utils.Converter import stringToAstExpr
from src.utils.ExprToPdf import generateResultPdf, createDigraphPdfFromTree
from src.utils.LuppoloArgParser import getParser
from src.grammar.LuppoloGrammar import LuppoloGrammar
from src.grammar.AntlrGrammarCompiler import AntlrGrammarCompiler
from src.interpreter.interpreter import LuppoloInterpreter
from src.ast.AstGenerator import AstGenerator

from test.LuppoloTester import LuppoloTester

def solveParsedArgs(parsed_args):
    match parsed_args.command:
        case "run":

            # Imposto il livello di logging
            loggingLevel = parsed_args.logging_level
            logger = LuppoloLogger('LuppoloLogger', LuppoloLogger.getLoggingLevelFromString(loggingLevel))
            LuppoloLogger.setCustomLogger(logger)

            # Estraggo gli argomenti
            sourceFilePath = parsed_args.source_file_path
            mainFunc = parsed_args.main_function
            args = parsed_args.args
            outputPdf = parsed_args.output_pdf
            outputConsole = parsed_args.output_console
            showPdf = parsed_args.show_pdf

            # Leggo il file sorgente e preparo il lexer ed il parser
            LuppoloLogger.logInfo(f"Reading source file {sourceFilePath} and initializing lexer and parser")
            fileContent = open(sourceFilePath, 'r').read()
            lexer = LuppoloGrammar.getLuppoloLexer(fileContent)
            parser = LuppoloGrammar.getLuppoloParser(lexer)

            # Effettuo il parsing del file sorgente
            LuppoloLogger.logInfo("Parsing the input")
            rawParsedTree = parser.program()

            # Genero l'AST
            LuppoloLogger.logInfo("Generating AST")
            astParsedTree = AstGenerator().visit(rawParsedTree)
            createDigraphPdfFromTree(astParsedTree, "astParsedTree")

            # Converto gli argomenti in espressioni dell'ast
            args = [stringToAstExpr(arg) for arg in args]

            # Interpreto il programma
            LuppoloLogger.logInfo("Interpreting the program")
            interpreter = LuppoloInterpreter(astParsedTree.children)
            result = interpreter.interpretFunc(mainFunc, args)

            # Genero il pdf
            if outputPdf != "none":
                LuppoloLogger.logInfo("Generating PDF")
                match outputPdf:
                    case "fullPdf":
                        pathFile = generateResultPdf(result)
                    case "onlyLatex":
                        pathFile = generateResultPdf(result, includeThreeGraph=False, includeRaw=False)
                    case "onlyGraph":
                        pathFile = generateResultPdf(result, includeLatex=False, includeRaw=False)
                    case "onlyRaw":
                        pathFile = generateResultPdf(result, includeLatex=False, includeThreeGraph=False)
                if showPdf:
                    LuppoloLogger.logInfo("Showing PDF")
                    os.system(f"start {pathFile}")
                    
            # Stampo il risultato
            if outputConsole != "none":
                LuppoloLogger.logInfo("Printing the result as "+outputConsole)
                print("Result:", end=" ")
                if outputConsole != "raw":
                    print(result.getLatexRapresentation())
                if outputConsole != "latex":
                    print(Trees.toStringTree(result))


        case "compile":
            
            # Estraggo gli argomenti
            syntaxFilePath = parsed_args.syntax_file_path
            antlrJarPath = parsed_args.antlr_jar_path

            # Controllo se il path del jar di antlr è stato specificato
            LuppoloLogger.logInfo("Compiling grammar using syntax file: "+syntaxFilePath+" and antlr jar: "+antlrJarPath)
            AntlrGrammarCompiler.compileGrammar(syntaxFilePath=syntaxFilePath, antlrJarPath=antlrJarPath)

        case "test":

            # Estraggo gli argomenti
            elements = parsed_args.elements
            typeTest = parsed_args.type_test

            testG = testI = True
            if elements == "grammar":
                testI = False
            elif elements == "interpreter":
                testG = False

            validT = erroneousT = True
            if typeTest == "valid":
                erroneousT = False
            elif typeTest == "erroneous":
                validT = False

            # Eseguo i test
            LuppoloLogger.logInfo("Running requested tests")
            if testG:
                LuppoloTester.testGrammar(validT, erroneousT)
            if testI:
                LuppoloTester.testInterpreter(validT, erroneousT)

            LuppoloLogger.logInfo("Tests completed")
        case _:
            print("Command not recognized")



if __name__ == "__main__":
    solveParsedArgs(getParser().parse_args())

