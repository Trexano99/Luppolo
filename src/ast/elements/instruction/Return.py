from src.ast.elements.expression.BaseExpr import BaseExpr
from src.ast.elements.instruction.BaseInstr import BaseInstr

class Return(BaseInstr):
    '''
    This class rapresent a return instruction node of the AST.
    '''

    __NODE_NAME = "RETURN"
    __ABBREV = "RET"

    def __init__(self, expression: BaseExpr):
        '''
        This method initializes the Return object.
        The method takes the following parameters:
        - expression: the expression to return.
        '''
        super().__init__(self.__NODE_NAME, [expression])

    def getPayload(self):
        return self.__ABBREV