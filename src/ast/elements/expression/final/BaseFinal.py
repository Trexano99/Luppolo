from abc import ABC
from src.ast.elements.expression.BaseExpr import BaseExpr

class BaseFinal(BaseExpr, ABC):
        '''
        This class rapresent the abstraction of a final leaf node of the AST.
        '''

        def __init__(self, name, value):
            '''
            This method initializes the BaseFinal object.
            The method takes the following parameters:
            - name: the name of the BaseFinal element.
            - value: the value of the BaseFinal element.
            '''
            super().__init__(name, [])
            self.value = value
    
        def getGraphRapresentation(self, graph, attributes=None):     
            if attributes is None: attributes = []
            attributes.append(("Value", self.value))
            return super().getGraphRapresentation(graph, attributes)
            
        def getPayload(self):
            return self.value