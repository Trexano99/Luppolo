from src.ast.BaseLuppNode import BaseLuppNode
from src.ast.elements.expression.BaseExpr import BaseExpr
from enum import Enum

class BinOp(BaseExpr):
        '''
        This class represents a binary operation in the AST.
        The allowed operators are chosen from the BinOpType Enum.
        '''
        
        __NODE_NAME = "BIN_OP"

        class BinOpType(Enum):
            '''This enum represents the allowed binary operators.'''
            SUM = "+"
            SUB = "-"
            MUL = "*"
            DIV = "/"
            POW = "^"
    
        def __init__(self, left:BaseLuppNode, op:BinOpType, right:BaseLuppNode):
            '''
            This method initializes the BinOp object.
            The method takes the following parameters:
            - op: the operator of the binary operation.
            - left: the left operand of the binary operation.
            - right: the right operand of the binary operation.
            '''
            assert isinstance(left, BaseExpr), "Left operand must be of type BaseLuppNode"  
            assert isinstance(right, BaseExpr), "Right operand must be of type BaseLuppNode"      
            super().__init__(self.__NODE_NAME, [left, right])
            self.op = op
    
        def getGraphRapresentation(self, graph, attributes=None):     
            if attributes is None: attributes = []
            attributes.append(("Operator", self.op.value))
            return super().getGraphRapresentation(graph, attributes)
            
        def getPayload(self):
            return self.op.name