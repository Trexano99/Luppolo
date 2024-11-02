from src.ast.elements.condition.BaseCond import BaseCond
from src.ast.elements.InstrBlock import InstrBlock
from src.ast.elements.instruction.BaseInstr import BaseInstr

class While(BaseInstr):
    '''
    This class rapresent a while instruction node of the AST.
    '''

    __NODE_NAME = "WHILE"
    __ABBREV = "WHL"

    def __init__(self, condition: BaseCond, block: InstrBlock):
        '''
        This method initializes the While object.
        The method takes the following parameters:
        - condition: the condition to check.
        - block: the block of instructions to execute.
        '''
        super().__init__(self.__NODE_NAME, [condition, block])

    def getPayload(self):
        return self.__ABBREV