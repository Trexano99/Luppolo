
from src.ast.elements.expression.BaseExpr import BaseExpr
from src.ast.elements.instruction.BaseInstr import BaseInstr
from src.ast.elements.expression.final.ID import ID

class Assignment(BaseInstr):
    '''
    This class rapresent an assignment instruction node of the AST.
    '''

    __NODE_NAME = "ASSIGNMENT"
    __ABBREV = "A"

    def __init__(self, varName:ID, expression: BaseExpr):
        '''
        This method initializes the Assignment object.
        The method takes the following parameters:
        - varName: the name of the variable.
        - expression: the expression to assign to the variable.
        '''
        super().__init__(self.__NODE_NAME, [expression])
        self.varName = varName

    def getGraphRapresentation(self, graph, attributes=None):     
        if attributes is None: attributes = []
        attributes.append(("VarName", self.varName.value))
        attributes.append(("VarType", self.varName.name))
        return super().getGraphRapresentation(graph, attributes)
        
    def getPayload(self):
        return self.__ABBREV