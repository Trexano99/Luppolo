

from src.ast.BaseLuppNode import BaseLuppNode
from abc import ABC

class BaseCond(BaseLuppNode, ABC):
    '''
    This class rapresent the abstraction of a condition node of the AST.
    '''
    
    __NODE_POSTFIX = "_COND"

    def __init__(self, name, children, negated = False):
        '''
        This method initializes the BaseCond object.
        The method takes the following parameters:
        - name: the name of the BaseCond element.
        - children: the children of the BaseCond element.
        - negated: a boolean indicator that rapresent the negation of the BaseCond element.
        '''
        super().__init__(name+self.__NODE_POSTFIX, children)
        self.negated = negated

    def inverseNegation(self):
        '''This method inverse the negation of the BaseCond element.'''
        self.negated = not self.negated


    def getGraphRapresentation(self, graph, attributes=None):     
        if attributes is None: attributes = []
        attributes.append(("Negated", self.negated))
        return super().getGraphRapresentation(graph, attributes)