
from src.expression.BaseLuppExpr import BaseLuppExpr
from math import gcd

class Rational(BaseLuppExpr):
    '''
    This class represents the Ractional node of the expression.
    Ractional number ar rappresentated as a fraction, where the 
    denominator can also be 1, giving a number with only a 
    numerator.
    '''

    def __init__(self, numerator: int, denominator: int = 1, negated = False):
        '''
        This method initializes the Rational object.
        The method takes the following parameters:
        - numerator: the numerator of the rational number.
        - denominator: the denominator of the rational number. Default is 1.
        '''
        self.numerator = numerator
        assert (denominator != 0), "Denominator cannot be 0"
        self.denominator = denominator
        self.__NODE_NAME = str(numerator) if denominator == 1 else str(numerator)+"/"+str(denominator)
        super().__init__(self.__NODE_NAME,[],negated)

    def getPayload(self):
        return self.__NODE_NAME
    
    def isZero(self):
        return self.numerator == 0
    
    def isOne(self):
        return (self.numerator == self.denominator and not self.negated) or \
               (abs(self.numerator) == abs(self.denominator) and self.negated)

    def getLatexRapresentation(self):
        sign = "-" if self.negated else ""
        if self.denominator == 1:
            return f"{sign}{self.numerator}"
        else:
            return f"{sign}\\frac{{{self.numerator}}}{{{self.denominator}}}"
        
    def inverseNegation(self):
        self.negated = not self.negated

    def simplify(self):
        common_divisor = gcd(self.numerator, self.denominator)
        simplified_num = self.numerator // common_divisor
        simplified_denom = self.denominator // common_divisor
        simplified_num = simplified_num if not self.negated else -simplified_num
        return Rational(simplified_num, simplified_denom)
        
    
    def __mul__(self, other):
        if isinstance(other, Rational):
            new_numerator = self.numerator * other.numerator
            new_denominator = self.denominator * other.denominator
            return Rational(new_numerator, new_denominator, self.negated != other.negated)
        else:
            raise TypeError("Multiplication is only supported between Rational objects")
    
    def __add__(self, other):
        if isinstance(other, Rational):
            common_denominator = self.denominator * other.denominator // gcd(self.denominator, other.denominator)
            adjusted_numerator_self = self.numerator * (common_denominator // self.denominator)
            adjusted_numerator_other = other.numerator * (common_denominator // other.denominator)
            new_numerator = adjusted_numerator_self + adjusted_numerator_other
            return Rational(new_numerator, common_denominator)
        else:
            raise TypeError("Addition is only supported between Rational objects")

    def __pow__(self, other):
        if isinstance(other, Rational):
            new_numerator = pow(self.numerator, other.numerator) ** (1 / other.denominator)
            new_denominator = pow(self.denominator, other.numerator) ** (1 / other.denominator)
            return Rational(new_numerator, new_denominator)
        else:
            raise TypeError("Power is only supported between Rational objects")
    

class Symbol(BaseLuppExpr):

    def __init__(self, char: str, negated = False):
        assert (char is not None), "char cannot be None"
        assert (len(char) == 1), "char must be a single character"
        self.__NODE_NAME = char
        super().__init__(self.__NODE_NAME,[],negated)

    def getPayload(self):
        return self.__NODE_NAME
    
    def getLatexRapresentation(self):
        return f"{'-' if self.negated else ''}{self.__NODE_NAME}"
    
    def simplify(self):
        return self