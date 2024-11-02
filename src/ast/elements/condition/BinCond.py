from src.ast.elements.condition.BaseCond import BaseCond
from src.ast.elements.expression.BaseExpr import BaseExpr
from enum import Enum

class BinCond(BaseCond):
        '''
        This class represents a binary condition in the AST.
        The allowed operators are chosen from the BinCondType Enum.
        '''
        
        __NODE_NAME = "BIN"

        class BinCondType(Enum):
            '''This enum represents the allowed binary operators.'''
            LEQ = "<="
            LESS = "<"
            EQ = "=="
            GREATER = ">"
            GEQ = ">="
    
        def __init__(self, op:BinCondType, left:BaseExpr, right:BaseExpr):
            '''
            This method initializes the BinCond object.
            The method takes the following parameters:
            - op: the operator of the binary condition.
            - left: the left operand of the binary condition.
            - right: the right operand of the binary condition.
            '''
            super().__init__(self.__NODE_NAME, [left, right])
            self.op = op
    
        def getGraphRapresentation(self, graph, attributes=None):     
            if attributes is None: attributes = []
            attributes.append(("Operator", self.op))
            return super().getGraphRapresentation(graph, attributes)
            
        def getPayload(self):
            return self.op.name