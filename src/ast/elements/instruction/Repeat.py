from src.ast.elements.expression.BaseExpr import BaseExpr
from src.ast.elements.InstrBlock import InstrBlock
from src.ast.elements.instruction.BaseInstr import BaseInstr

class Repeat(BaseInstr):
    '''
    This class rapresent a repeat instruction node of the AST.
    '''

    __NODE_NAME = "REPEAT"
    __ABBREV = "RPT"

    def __init__(self, expression: BaseExpr, block: InstrBlock):
        '''
        This method initializes the Repeat object.
        The method takes the following parameters:
        - expression: the number of times to repeat the block.
        - block: the block of instructions to repeat.
        '''
        super().__init__(self.__NODE_NAME, [expression, block])
    
    def getPayload(self):
        return self.__ABBREV