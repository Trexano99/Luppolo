

from src.ast.BaseLuppNode import BaseLuppNode
from src.ast.elements.final.BaseFinal import BaseFinal

class Call(BaseFinal):

    __NODE_NAME = "CALL"

    def __init__(self, funcCall:str):
        '''
        This method initializes the Call object, a function call.
        The method takes the following parameters:
        - funcCall: the name of the function to Call.
        '''
        assert (funcCall is not None), "Name cannot be None"
        super().__init__(self.__NODE_NAME, funcCall)