from src.ast.elements.condition.BaseCond import BaseCond
from enum import Enum

class AndOr(BaseCond):
        '''
        This class represents a binary condition in the AST.
        The allowed operators are chosen from the AndOrType Enum.
        '''
        
        __NODE_NAME = "ANDOR"

        class AndOrType(Enum):
            '''This enum represents the allowed binary operators.'''
            AND = "&&"
            OR = "||"
    
        def __init__(self, op:AndOrType, left:BaseCond, right:BaseCond):
            '''
            This method initializes the AndOr object.
            The method takes the following parameters:
            - op: the operator of the binary condition.
            - left: the left condition.
            - right: the right condition.
            '''
            super().__init__(self.__NODE_NAME, [left, right])
            self.op = op
    
        def getGraphRapresentation(self, graph, attributes=None):     
            if attributes is None: attributes = []
            attributes.append(("Operator", self.op))
            return super().getGraphRapresentation(graph, attributes)
            
        def getPayload(self):
            return self.op.name