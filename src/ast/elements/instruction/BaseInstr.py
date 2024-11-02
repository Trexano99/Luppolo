

from src.ast.BaseLuppNode import BaseLuppNode
from abc import ABC

class BaseInstr(BaseLuppNode, ABC):
    
    __NODE_POSTFIX = "_INSTR"

    def __init__(self, name, children, negated = False):
        super().__init__(name+self.__NODE_POSTFIX, children)