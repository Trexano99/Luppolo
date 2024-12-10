

import argparse

def getParser():
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
        help="The path of the ANTLR4 jar file. Default value is '%%ANTLR4_JAR%%'"
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
        help="The type of test to run. Default value is 'all'"
    )
    
    return parser