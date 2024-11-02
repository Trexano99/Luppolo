
from src.ast.BaseLuppNode import BaseLuppNode
from src.ast.elements.Function import Function
from graphviz import Digraph

class Program(BaseLuppNode):
    '''
    This class represents the Program node of the AST.
    '''

    __NODE_NAME = "PROGRAM"
    __ABBREV = "P"

    def __init__(self, functions: list[Function]):
        '''
        This method initializes the Program object.
        The method takes the following parameters:
        - functions: the list of functions of the program.
        '''
        super().__init__(self.__NODE_NAME, functions)

    def addFunction(self, function: Function):
        '''
        This method adds a function to the program.
        The method takes the following parameters:
        - function: the function to add.
        '''
        self.addChild(function)
    
    def getPayload(self):
        return self.__ABBREV