import argparse, os

from antlr4.tree.Trees import Trees

from src.utils.LuppoloLogger import LuppoloLogger
from src.utils.Converter import stringToAstExpr
from src.utils.ExprToPdf import generateResultPdf, createDigraphPdfFromTree
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


def main():
    parser = argparse.ArgumentParser(description="Luppolo Interpreter")
    subparsers = parser.add_subparsers(dest="command")

    # Definisco il comando run per eseguire l'interprete
    run_parser = subparsers.add_parser("run", help="Run the interpreter with the specified arguments")
    
    run_parser.add_argument(
        "source_file_path",
        help="The path of the luppolo file to interpret. It must be a .lp file"
    )

    run_parser.add_argument(
        "args",
        nargs="*",
        help="The arguments to pass to the Main function of the interpreter"
    )

    run_parser.add_argument(
        "--main-function",
        "-mf",
        default="Main",
        help="The name of the main function to run. Default value is 'Main'"
    )

    run_parser.add_argument(
        "--output-pdf",
        "-opdf",
        default="fullPdf",
        choices=["fullPdf", "onlyLatex", "onlyGraph", "onlyRaw", "none"],
        help="To generate a pdf file as output. Require pdflatex installed if latex needed. Default value is 'fullPdf'"
    )

    run_parser.add_argument(
        "--show-pdf",
        default=True,
        choices=[True, False],
        help="To show the generated pdf at the end of the execution if it has been generated. Default value is 'True'"
    )

    run_parser.add_argument(
        "--output-console",
        "-oc",
        default="latex",
        choices=["latex", "raw", "both", "none"],
        help="How the output should be printend in console. Default value is 'latex'"
    )

    run_parser.add_argument(
        "--logging-level",
        "-ll",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="The logging level of Luppolo. Default value is 'INFO'"
    )


    # Definisco il comando compile per compilare la grammatica
    compiler_parser = subparsers.add_parser("compile", help="Compile the Luppolo grammar")
    
    # Aggiungo gli argomenti per il comando compile
    compiler_parser.add_argument(
        "--syntax-file-path",
        "-sfp",
        default="src\\grammar\\syntax\\luppolo.g",
        nargs="*",
        help="The path of the grammar file to compile. Default value is 'src\\grammar\\syntax\\luppolo.g'"
    )

    compiler_parser.add_argument(
        "--antlr-jar-path",
        "-ajp",
        default="%ANTLR4_JAR%",
        nargs="*",
        help="The path of the ANTLR4 jar file. Default value is '%ANTLR4_JAR%'"
    )

    # Definisco il comando test per eseguire i test
    test_parser = subparsers.add_parser("test", help="Run the Luppolo tests")

    test_parser.add_argument(
        "--elements",
        "-e",
        default="all",
        choices=["all", "grammar", "interpreter"],
        help="The elements to test. Default value is 'all'"
    )

    test_parser.add_argument(
        "--type-test",
        "-tt",
        default="all",
        choices=["all", "valid", "erroneous"],
    )


    # Parso gli argomenti
    parsed_args = parser.parse_args()

    # Chiamo la funzione corretta in base al comando
    solveParsedArgs(parsed_args)

if __name__ == "__main__":
    main()

