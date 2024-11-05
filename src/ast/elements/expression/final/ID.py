

from src.ast.elements.expression.final.BaseFinal import BaseFinal

class ID(BaseFinal):

    __NODE_NAME = "ID"

    def __init__(self, varName:str):
        '''
        This method initializes the ID object, a string of characters with the capital letter.
        The method takes the following parameters:
        - varName: the varName of the ID.
        '''
        assert (varName is not None), "varName cannot be None"
        assert (varName[0].isupper()), "varName must start with an uppercase letter"
        super().__init__(self.__NODE_NAME, varName)