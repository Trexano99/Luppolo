
from src.ast.elements.InstrBlock import InstrBlock
from src.ast.BaseLuppNode import BaseLuppNode
from src.ast.elements.final.ID import ID

class Function(BaseLuppNode):
    '''
    This class represents a Function node of the AST.
    '''

    __NODE_NAME = "FUNCTION"
    __ABBREV = "F"

    def __init__(self, funcName:ID, funcParams:list[ID], instructions: InstrBlock):
        '''
        This method initializes the Function object.
        The method takes the following parameters:
        - funcName: the name of the function.
        - funcParams: the list of parameters of the function.
        - instructions: the list of instructions of the function.
        '''
        super().__init__(self.__NODE_NAME, instructions)
        self.funcName = funcName
        self.funcParams = funcParams

    def getGraphRapresentation(self, graph, attributes=None):     
        if attributes is None: attributes = []
        attributes.append(("Name", self.funcName.name))
        attributes.append(("Params", self.getParamsAsString()))
        return super().getGraphRapresentation(graph, attributes)
        
    def getPayload(self):
        return self.__ABBREV
    
    def getParamsAsString(self):
        '''Return the list of parameters as a string'''
        return "".join([f"{param.name}, " for param in self.funcParams])[:-2]