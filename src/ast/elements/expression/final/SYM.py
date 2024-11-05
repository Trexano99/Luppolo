

from src.ast.elements.expression.final.BaseFinal import BaseFinal

class SYM(BaseFinal):

    __NODE_NAME = "SYM"

    def __init__(self, name:str):
        '''
        This method initializes the SYM object, a single character symbol.
        The method takes the following parameters:
        - name: the name of the SYM.
        '''
        assert (name is not None), "Name cannot be None"
        assert (len(name)==1), "Name must be a single character"
        assert (name[0].islower()), "Name must start with an uppercase letter"
        super().__init__(self.__NODE_NAME, name)