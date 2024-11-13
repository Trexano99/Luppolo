from src.utils.GenericTreeNode import GenericTreeNode
from abc import abstractmethod
from functools import reduce

class BaseLuppExpr(GenericTreeNode): 
    '''
    BaseLuppExpr are final nodes and must not be edited after creation.
    ''' 

    def __init__(self, name, children: list = None, negated = False):
        all(isinstance(addend, BaseLuppExpr) for addend in children), "all elements in addends must be BaseLuppExpr"
        #Se non sei una potenza, ordino i figli
        if self.__class__.__name__ != "Pow":
            children.sort()
        super().__init__(name, children)
        self.negated = negated


    @abstractmethod
    def getLatexRapresentation(self):
        '''
        This method is used to get the latex repr
        esentation of the node.
        '''
        pass

    def simplify(self):
        '''
        This method is used to apply some base common semplifications to the node.
        All the children are going to be simplified and if all children are rational, 
        the nodes is going to be simplified to a rational.
        If semplifications are not applicable, the method returns None.
        '''
        # Simplify all childrens
        self.children = [child.simplify() for child in self.children]

        # Semplify to ractional if all children are rational
        if len(self.children) > 0 and all([child.__class__.__name__ == "Rational" for child in self.children]):
            
            operations = {
                'Add': lambda x, y: x + y,
                'Mult': lambda x, y: x * y,
                'Pow': lambda x, y: x ** y
            }
            # Apply the operation to the children and get a rational result
            rationalResult = reduce(operations[self.__class__.__name__], self.children)
            # If the node is negated, invert the negation on the result and call simplify
            if self.negated: rationalResult.inverseNegation()
            return rationalResult.simplify()
        
        return None
    

    @staticmethod
    def baseSimpl(method):
        '''
        This wrapper is created to call the simplify method of the base node 
        and if the result is None, call the method passed as parameter.
        '''
        def wrapper(self, *args, **kwargs):
            res = super(self.__class__, self).simplify()
            if res is not None:
                return res
            return method(self, *args, **kwargs)
        return wrapper

    def __lt__(self, other):
        '''
        This method is used to compare two nodes.
        '''
        if self.__class__.__name__ == other.__class__.__name__:
            return self.children < other.children
        return self.type_priority[self.__class__.__name__] < self.type_priority[other.__class__.__name__]

    type_priority = {
            'Rational': 1,
            'Mult': 2,
            'Pow': 3,
            'Symbol': 4,
            'Add': 5
        }
    
    def __eq__(self, value: object) -> bool:
        return isinstance(value, BaseLuppExpr) and \
               type(self) == type(value) and \
               super().__eq__(value) and \
               self.negated == value.negated

    def __hash__(self):
        return hash((self.name, tuple(self.children), self.negated))