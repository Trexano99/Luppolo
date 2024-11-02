
from src.ast.BaseLuppNode import BaseLuppNode

class InstrBlock(BaseLuppNode):
    '''
    This class represents an instruction block node of the AST.
    '''

    __NODE_NAME = "INSTR_BLOCK"
    __ABBREV = "BLK"

    def __init__(self, instructions: list[BaseLuppNode]):
        '''
        This method initializes the InstrBlock object.
        The method takes the following parameters:
        - instructions: the list of instructions of the block.
        '''
        super().__init__(self.__NODE_NAME, instructions)
    
    def getPayload(self):
        return self.__ABBREV
