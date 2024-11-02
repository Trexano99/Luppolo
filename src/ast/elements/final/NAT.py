

from src.ast.BaseLuppNode import BaseLuppNode
from src.ast.elements.final.BaseFinal import BaseFinal

class NAT(BaseFinal):

    __NODE_NAME = "NAT"

    def __init__(self, value:str):
        '''
        This method initializes the NAT object, a natural number.
        The method takes the following parameters:
        - value: the value of the NAT.
        '''
        assert (value is not None), "value cannot be None"
        assert (value.isnumeric()), "value must be a number"
        super().__init__(self.__NODE_value, value)