
from src.expression.BaseLuppExpr import BaseLuppExpr
from math import gcd

class Rational(BaseLuppExpr):
    '''
    This class represents the Ractional node of the expression.
    Ractional number ar rappresentated as a fraction where the 
    denominator can also be 1 rapresenting an integer.
    '''

    def __init__(self, numerator: int, denominator: int = 1, negated = False):
        '''
        This method initializes the Rational object. Numerator and denominator
        are stored as integers, and the negated flag is stored as a boolean.
        The negation at numerator and denominator level is brought to the node level.
        The method takes the following parameters:
        - numerator: the integer numerator of the rational number.
        - denominator: the integer denominator of the rational number. Default is 1. Cannot be 0.
        - negated: indicate if the rational number is negated. Default is False.
        '''
        assert (denominator != 0), "Denominator cannot be 0"

        # Porto la negazione a livello di nodo e non dei valori
        negated = negated != ((numerator < 0) != (denominator < 0))
        self.numerator = int(abs(numerator))
        self.denominator = int(abs(denominator))

        self.__NODE_NAME = str(self.numerator) if denominator == 1 else str(self.numerator)+"/"+str(self.denominator)
        super().__init__(self.__NODE_NAME,[],negated)

    def copy_with(self, numerator = None, denominator = None, negated = None):
        return Rational(
            numerator = self.numerator if numerator is None else numerator,
            denominator = self.denominator if denominator is None else denominator,
            negated = self.negated if negated is None else negated
        )

    def getPayload(self):
        return self.__NODE_NAME
    
    def isZero(self):
        '''
        This method is used to check if the rational number is zero.
        '''
        return self.numerator == 0
    
    def isOne(self):
        '''
        This method is used to check if the rational number is one.
        '''
        if self.numerator == self.denominator and self.negated: return False
        return (self.numerator == self.denominator and not self.negated) or \
               (abs(self.numerator) == abs(self.denominator) and self.negated)

    def getLatexRapresentation(self):
        sign = "-" if self.negated else ""
        if self.denominator == 1:
            return f"{sign}{self.numerator}"
        else:
            return f"{sign}\\frac{{{self.numerator}}}{{{self.denominator}}}"

    def simplify(self):
        common_divisor = gcd(self.numerator, self.denominator)
        simplified_num = self.numerator // common_divisor
        simplified_denom = self.denominator // common_divisor
        simplified_num = simplified_num if not self.negated else -simplified_num
        return Rational(simplified_num, simplified_denom)
        
    
    def __mul__(self, other):
        '''
        This method is used to multiply a rational number with another rational number.
        The method returns a new Rational object with the calculated numerator and denominator.
        Parameters:
        - other: the Rational object to multiply with.
        '''
        if isinstance(other, Rational):
            new_numerator = self.numerator * other.numerator
            new_denominator = self.denominator * other.denominator
            return Rational(new_numerator, new_denominator, self.negated != other.negated)
        else:
            raise TypeError("Multiplication is only supported between Rational objects")
    
    def __add__(self, other):
        '''
        This method is used to add a rational number with another rational number.
        For the denominator, the method calculates the least common multiple between the two denominators
        and then calculates the new numerator accordingly.
        Note that if the resulting numerator or denominator has decimal value them will be truncated
        from the Rational object, giving an approximate value.
        Parameters:
        - other: the Rational object to add with.
        '''
        if isinstance(other, Rational):
            self_numerator = self.numerator if not self.negated else -self.numerator
            other_numerator = other.numerator if not other.negated else -other.numerator
            common_denominator = self.denominator * other.denominator // gcd(self.denominator, other.denominator)
            adjusted_numerator_self = self_numerator * (common_denominator // self.denominator)
            adjusted_numerator_other = other_numerator * (common_denominator // other.denominator)
            new_numerator = adjusted_numerator_self + adjusted_numerator_other
            return Rational(new_numerator, common_denominator)
        else:
            raise TypeError("Addition is only supported between Rational objects")

    def __pow__(self, other):
        '''
        This method is used to calculate the power of a rational number with another rational number.
        If the result is an exact integer, the method returns a Rational object with the integer value.
        Otherwise, the method returns a Rational object with the calculated numerator and denominator.
        Note that if the resulting numerator or denominator has decimal value them will be truncated
        from the Rational object, giving an approximate value.
        Parameters:
        - other: the Rational object to calculate the power with.
        '''
        if isinstance(other, Rational):
            expValue = other.numerator / other.denominator * (1 if not other.negated else -1)
            numerator = self.numerator ** expValue
            denominator = self.denominator ** expValue
            if numerator / denominator == int(numerator / denominator):
                return Rational(int(numerator / denominator))
            return Rational(numerator, denominator)
        else:
            raise TypeError("Power is only supported between Rational objects")
        
    @BaseLuppExpr.baseDerive
    def derive(self, symbol):
        return Rational(0)
    

class Symbol(BaseLuppExpr):
    '''
    This class represents the Symbol node of the expression.
    Symbol nodes are used to represent variables or constants.
    '''

    def __init__(self, char: str, negated = False):
        '''
        This method initializes the Symbol object. The name of the symbol is stored as a string,
        and the negated flag is stored as a boolean.
        The method takes the following parameters:
        - char: the name of the symbol. Must be a single alphabetic character.
        '''

        assert (char is not None), "char cannot be None"
        assert (len(char) == 1), "char must be a single character"
        assert (char.isalpha()), "char must be a letter"
        self.__NODE_NAME = char
        super().__init__(self.__NODE_NAME,[],negated)

    def copy_with(self, char = None, negated = None):
        return Symbol(
            char = self.__NODE_NAME if char is None else char,
            negated = self.negated if negated is None else negated
        )

    def getPayload(self):
        return self.__NODE_NAME
    
    def getLatexRapresentation(self):
        return f"{'-' if self.negated else ''}{self.__NODE_NAME}"
    
    def simplify(self):
        return self
    
    @BaseLuppExpr.baseDerive
    def derive(self, symbol):
        return Rational(1) if self == symbol else Rational(0)