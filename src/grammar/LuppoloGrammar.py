
from antlr4 import CommonTokenStream, InputStream
from bin.grammar.syntax import luppoloLexer, luppoloParser, luppoloListener, luppoloVisitor
from antlr4.error.ErrorListener import ErrorListener
from src.utils.LuppoloLogger import LuppoloLogger

class LuppoloGrammar:
    '''
    This class is used to import the generated classes from the grammar.
    '''

    luppoloLexer = luppoloLexer.luppoloLexer
    luppoloParser = luppoloParser.luppoloParser
    luppoloListener = luppoloListener.luppoloListener
    luppoloVisitor = luppoloVisitor.luppoloVisitor

    @staticmethod
    def getLuppoloLexer(fileContent):
        lexer = LuppoloGrammar.luppoloLexer(InputStream(fileContent))
        lexer.removeErrorListeners()
        lexer.addErrorListener(LuppoloErrorListener("Lexer"))
        return lexer
    
    @staticmethod
    def getLuppoloParser(lexer):
        parser = LuppoloGrammar.luppoloParser(CommonTokenStream(lexer))
        parser.removeErrorListeners()
        parser.addErrorListener(LuppoloErrorListener("Parser"))
        return parser

class LuppoloErrorListener(ErrorListener):

    def __init__(self, sourceErr):
        self.sourceErr = sourceErr
        super().__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):

        lineError = recognizer.getInputStream().tokenSource.inputStream.strdata.splitlines()[line-1]

        commonErrorString = f"Detected by {self.sourceErr} - At line {line}, column {column} in {self.sourceErr}:\n{lineError}\n{' '*(column-1)}^\n{msg}"

        if e is not None:
            LuppoloLogger.logError(commonErrorString)
            raise Exception(e)
        else:
            LuppoloLogger.logWarning(commonErrorString)
            raise Exception("Fix the warning. Not allowed.")
        