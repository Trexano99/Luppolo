from src.ast.elements.condition.BaseCond import BaseCond
from src.ast.elements.InstrBlock import InstrBlock
from src.ast.elements.instruction.BaseInstr import BaseInstr

class IfElse(BaseInstr):
    '''
    This class rapresent a if else instruction node of the AST.
    '''

    __NODE_NAME = "IFELSE"
    __ABBREV = "IFEL"


    def __init__(self, condition: BaseCond, trueBlock: InstrBlock, falseBlock: InstrBlock = None):
        '''
        This method initializes the IfElse object.
        The method takes the following parameters:
        - condition: the condition to check.
        - trueBlock: the block of instructions to execute if the condition is true.
        - falseBlock: the block of instructions to execute if the condition is false.
        '''
        child = [condition, trueBlock]
        condition.name = "CONDITION"
        trueBlock.name = "TRUE_BLOCK"
        if falseBlock is not None:
            child.append(falseBlock)
            falseBlock.name = "FALSE_BLOCK"
        super().__init__(self.__NODE_NAME, child)
    
    def getPayload(self):
        return self.__ABBREV
