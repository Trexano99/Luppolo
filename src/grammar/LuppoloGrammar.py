
from bin.grammar.syntax import luppoloLexer, luppoloParser, luppoloListener, luppoloVisitor

class LuppoloGrammar:
    '''
    This class is used to import the generated classes from the grammar.
    '''

    luppoloLexer = luppoloLexer.luppoloLexer
    luppoloParser = luppoloParser.luppoloParser
    luppoloListener = luppoloListener.luppoloListener
    luppoloVisitor = luppoloVisitor.luppoloVisitor

    