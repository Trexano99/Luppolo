

from src.ast.BaseLuppNode import BaseLuppNode
from abc import ABC

class BaseExpr(BaseLuppNode, ABC):
    '''
    This class rapresent the abstraction of an expression node of the AST.
    '''
    
    __NODE_POSTFIX = "_EXPR"

    def __init__(self, name, children, negated = False):
        '''
        This method initializes the BaseExpr object.
        The method takes the following parameters:
        - name: the name of the BaseExpr element.
        - children: the children of the BaseExpr element.
        - negated: a boolean indicator that rapresent the negation of the BaseExpr element.
        '''
        super().__init__(name+self.__NODE_POSTFIX, children)
        self.negated = negated

    def inverseNegation(self):
        '''This method inverse the negation of the BaseExpr element.'''
        self.negated = not self.negated


    def getGraphRapresentation(self, graph, attributes=None):     
        if attributes is None: attributes = []
        attributes.append(("Negated", self.negated))
        return super().getGraphRapresentation(graph, attributes)