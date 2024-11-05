

from src.ast.elements.expression.final.ID import ID
from src.ast.elements.expression.BaseExpr import BaseExpr
from src.ast.BaseLuppNode import BaseLuppNode

class FuncCall(BaseLuppNode):
    '''
    This class rapresent a function call node of the AST.
    '''

    __NODE_NAME = "FUN_CALL"

    def __init__(self, funcName:ID, args:list[BaseExpr]):
        '''
        This method initializes the FuncCall object, a function call.
        The method takes the following parameters:
        - funcName: the name of the function to call.
        - args: the arguments of the function call.
        '''
        assert (funcName is not None), "funcName cannot be None"
        super().__init__(self.__NODE_NAME, args)
        self.funcName = funcName.value


    def getGraphRapresentation(self, graph, attributes=None):     
        if attributes is None: attributes = []
        attributes.append(("Function Name", self.funcName))
        return super().getGraphRapresentation(graph, attributes)
    
    def getPayload(self):
        return self.__NODE_NAME