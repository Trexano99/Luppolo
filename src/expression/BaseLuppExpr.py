from src.utils.GenericTreeNode import GenericTreeNode
from abc import abstractmethod, ABC
from functools import reduce

class BaseLuppExpr(GenericTreeNode): 
    '''
    This class rapresent a generic rapresentation of an expression node.
    BaseLuppExpr are final nodes and must not be edited after creation.
    ''' 

    def __init__(self, name, children: list = None, negated = False):
        '''
        This method initializes the BaseLuppExpr object. The method takes the following parameters:
        - name: the name of the node.
        - children: the list of children of the node. Default is None. All must be of type BaseLuppExpr.
        - negated: indicate if the node is negated. Default is False.
        '''

        children = [child.copy_with() for child in children] if children is not None else []
        all(isinstance(child, BaseLuppExpr) for child in children), "all elements in children must be of type BaseLuppExpr"
        #Se non sei una potenza, ordino i figli. Nella potenza infatti il primo figlio è la base e il secondo l'esponente
        if self.__class__.__name__ != "Pow":
            children.sort()
        name = ("-" + name) if negated else name
        super().__init__(name, children)
        self.negated = negated

    @abstractmethod
    def copy_with(self, **kwargs):
        '''
        This method is used to create a copy of the node with the overwrited specified parameters.
        '''
        pass

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
            
            if self.__class__.__name__ == "Pow":
                rationalResult, approx = self.children[0] ** self.children[1]
                return rationalResult if not approx else None
            
            operations = {
                'Add': lambda x, y: x + y,
                'Mult': lambda x, y: x * y
            }
            # Apply the operation to the children and get a rational result
            rationalResult = reduce(operations[self.__class__.__name__], self.children)

                
            # If the node is negated, invert the negation on the result and call simplify
            return rationalResult.copy_with(negated = self.negated != rationalResult.negated).simplify()
        
        return None
    
    def expand(self):
        '''
        This method is used to manipulate the node expanding the node due
        to the properties of sum, product and power.
        '''
        return self.copy_with()
    
    
    def substitute(self, toBeSubstitue, substitute):
        '''
        This method is used to substitute a node with another node.
        The method takes the following parameters:
        - toBeSubstitue: the node to be substituted.
        - substitute: the node to substitute.
        '''
        self.children = [child.substitute(toBeSubstitue, substitute) for child in self.children]
        if self == toBeSubstitue:
            return substitute
        return self
    
    
    def derive(self, symbol):
        '''
        This method is used to derive the node with respect to a symbol.
        The method takes the following parameters:
        - symbol: the symbol to derive the node with respect to.
        '''
        pass

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
    

    @staticmethod
    def baseExpansion(method):
        '''
        This wrapper is created to call the expand on all the children of the node
        before calling the method passed as parameter.
        '''
        def wrapper(self, *args, **kwargs):
            print("Expanding element of class: ", self.__class__.__name__)
            self.children = [child.expand() for child in self.children]
            return method(self, *args, **kwargs)
        return wrapper
    

    @staticmethod
    def baseDerive(method):
        '''
        This wrapper is created to call the derive on all the children of the node
        before calling the method passed as parameter.
        '''
        def wrapper(self, *args, **kwargs):
            symbol=args[0]
            assert symbol.__class__.__name__ == "Symbol", "The symbol must be a Symbol isntance"
            return method(self, *args, **kwargs)
        return wrapper


    def __lt__(self, other):
        '''
        This method is used to compare two nodes.
        '''
        if self.__class__.__name__ == other.__class__.__name__:
            if len(self.children)>0:
                return self.children < other.children
            return self.name < other.name
        return self.type_priority[self.__class__.__name__] < self.type_priority[other.__class__.__name__]


    def __eq__(self, value: object) -> bool:
        return isinstance(value, BaseLuppExpr) and \
               type(self) == type(value) and \
               super().__eq__(value) and \
               self.negated == value.negated

    def __hash__(self):
        return hash((self.name, tuple(self.children), self.negated))
    
    
    type_priority = {
            'Rational': 1,
            'Mult': 2,
            'Pow': 3,
            'Symbol': 4,
            'Add': 5
        }