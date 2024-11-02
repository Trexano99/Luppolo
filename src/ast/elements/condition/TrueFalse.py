from src.ast.elements.condition.BaseCond import BaseCond
from src.ast.elements.expression.BaseExpr import BaseExpr
from enum import Enum

class TrueFalse(BaseCond):
        '''
        This class represents a binary condition in the AST.
        The allowed operators are chosen from the TrueFalseType Enum.
        '''
        
        __NODE_NAME = "T/F"

        class TrueFalseType(Enum):
            '''This enum represents the allowed binary operators.'''
            TRUE = "true"
            FALSE = "false"

        def __init__(self, value:TrueFalseType):
            '''
            This method initializes the TrueFalse object.
            The method takes the following parameters:
            - op: the operator of the binary condition.
            '''
            super().__init__(self.__NODE_NAME, [])
            self.value = value

        def getGraphRapresentation(self, graph, attributes=None):
            if attributes is None: attributes = []
            attributes.append(("Value", self.value))
            return super().getGraphRapresentation(graph, attributes)
        
        def getPayload(self):
            return self.value.name