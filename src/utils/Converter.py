

from src.grammar.LuppoloGrammar import LuppoloGrammar
from src.ast.AstGenerator import AstGenerator
from antlr4 import InputStream, CommonTokenStream

def stringToAstExpr(string):
    '''
    This function converts any expression string to an AST expression.
    It uses the luppolo lexer and parser, so ensure to have the grammar 
    compiled before using this function.
    '''

    tempProgram = "Main(){A="+string+"}"

    lexer = LuppoloGrammar.luppoloLexer(InputStream(tempProgram))
    parser = LuppoloGrammar.luppoloParser(CommonTokenStream(lexer))

    try:
        tree = parser.program()
        astTree = AstGenerator().visit(tree)
        exprConverted = astTree.children[0].children[0].children[0].children[0]
        return exprConverted
    except Exception as e:
        print(f"Error while converting the string {string} to an AST expression: " + str(e))
        raise e