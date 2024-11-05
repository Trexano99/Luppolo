
from src.ast.elements.InstrBlock import InstrBlock
from src.ast.elements.expression.BaseExpr import BaseExpr
from src.ast.elements.instruction.BaseInstr import BaseInstr
from src.ast.elements.expression.final.ID import ID

class Foreach(BaseInstr):
    '''
    This class rapresent a foreach instruction node of the AST.
    '''

    __NODE_NAME = "FOREACH"
    __ABBREV = "FEACH"

    def __init__(self, varName:ID, expression: BaseExpr, instrBlock: InstrBlock):
        '''
        This method initializes the Foreach object.
        The method takes the following parameters:
        - varName: the name of the variable.
        - expression: the expression to assign to the variable.
        - block: the block of instructions to execute.
        '''
        super().__init__(self.__NODE_NAME, [expression, instrBlock])
        self.varName = varName

    def getGraphRapresentation(self, graph, attributes=None):
        if attributes is None: attributes = []
        attributes.append(("VarName", self.varName.value))
        attributes.append(("VarType", self.varName.name))
        return super().getGraphRapresentation(graph, attributes)