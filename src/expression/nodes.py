
from abc import ABC, abstractmethod
from functools import reduce

from src.expression.BaseLuppExpr import BaseLuppExpr
from src.expression.leaf import Rational

class Add(BaseLuppExpr):
    '''
    This class represents the Add node of the expression.
    The Add node is used to represent the sum of two or more elements.
    '''

    __NODE_NAME = "Add"
    __ABBREV = "S"

    def __init__(self, addends: list, negated = False):
        '''
        This method initializes the Add object.
        The method takes the following parameters:
        - addends: the list of addends of the sum. Must be at least two elements.
        - negated: a boolean flag that indicates if the sum is negated. Default is False.
        '''
        assert (addends is not None), "addends cannot be None"
        assert (len(addends) > 1), "addends must be at least two elements"
        super().__init__(self.__NODE_NAME, addends, negated)

    def copy_with(self, addends = None, negated = None):
        return Add(
            addends = self.children if addends is None else addends,
            negated = self.negated if negated is None else negated
        )

    def getPayload(self):
        return self.__ABBREV
    
    def getLatexRapresentation(self):
        sign = "-" if self.negated else ""
        core = self.children[0].getLatexRapresentation()
        for child in self.children[1:]:
            # Se il figlio è negato, aggiungo il segno davanti
            core += ("" if child.negated else "+") + child.getLatexRapresentation()
        # Se il nodo è negato o il padre è una moltiplicazione o una potenza, aggiungo le parentesi
        if self.negated or (self.parent is not None and (isinstance(self.parent, Mult) or isinstance(self.parent, Pow))):
            core = f"\\left({core}\\right)"
        return sign + core
    
    @BaseLuppExpr.baseSimpl
    def simplify(self):
        children = []
        cumulatedSum = Rational(0)
        multiplicativeFactors = {}
        for addend in self.children:
            # Se uno degli addendi è una somma, aggiungo i suoi addendi
            if isinstance(addend, Add):
                if addend.negated:
                    children.extend([child.copy_with(negated = not child.negated) for child in addend.children])
                else:
                    children.extend(addend.children)
            # Se uno degli addendi è un razionale, lo aggiungo alla somma cumulata
            elif isinstance(addend, Rational):
                cumulatedSum += addend
            # Se uno degli addendi è un prodotto con un razionale davanti, 
            # aggiungi il prodotto alla lista dei fattori moltiplicativi
            else:
                rationalPart = Rational(1, negated = addend.negated)
                addend = addend.copy_with(negated = False)
                # Se è una moltiplicazione e c'è un razionale davanti
                if isinstance(addend, Mult) and isinstance(addend.children[0], Rational):
                    rationalPart *= addend.children[0]
                    addend = addend.children[1] if len(addend.children) == 2 else Mult(addend.children[1:])

                if addend in multiplicativeFactors:
                    multiplicativeFactors[addend] += rationalPart
                else:
                    multiplicativeFactors[addend] = rationalPart

        # Se la somma cumulata non è zero, aggiungila alla lista degli addendi
        if not cumulatedSum.isZero():
            children.append(cumulatedSum)
        # Aggiungi i fattori moltiplicativi alla lista degli addendi
        for factor, rational in multiplicativeFactors.items():
            # Se il razionale è uno appendo solo il fattore
            if rational.isOne():
                children.append(factor)
            # Se il razionale è -1, appendo il fattore con la negazione invertita
            elif rational.copy_with(negated = False).isOne():
                children.append(factor.copy_with(negated = not factor.negated))
            # Altrimenti appendo il prodotto tra il razionale e il fattore
            else:
                children.append(Mult([rational, factor]).simplify())
        
        # Se la lista degli addendi è vuota, ritorna zero
        if len(children) == 0:
            return Rational(0)
        
        # Se c'è più di un addendo, ritorna un nuovo addendo
        if len(children) > 1:
            return Add(children, self.negated)
        
        return children[0].copy_with(negated = self.negated != children[0].negated)
    
    @BaseLuppExpr.baseExpansion
    def expand(self):
        if self.negated:
            return Add([child.expand().copy_with(negated = not child.negated) for child in self.children])
        return Add(self.children, self.negated)
    
    @BaseLuppExpr.baseDerive
    def derive(self, symbol):
        return Add([child.derive(symbol) for child in self.children], self.negated).simplify()
    
        

class Mult(BaseLuppExpr):
    '''
    This class represents the Mult node of the expression.
    The Mult node is used to represent the product of two or more elements.
    '''

    __NODE_NAME = "Mul"
    __ABBREV = "M"

    def __init__(self, factors: list, negated = False):
        '''
        This method initializes the Mult object.
        The method takes the following parameters:
        - factors: the list of factors of the product. Must be at least two elements.
        - negated: a boolean flag that indicates if the product is negated. Default is False.
        '''

        assert (factors is not None), "factors cannot be None"
        assert (len(factors) > 1), "factors must be at least two elements"
        super().__init__(self.__NODE_NAME, factors, negated)

    def copy_with(self, factors = None, negated = None):
        return Mult(
            factors = self.children if factors is None else factors,
            negated = self.negated if negated is None else negated
        )

    def getPayload(self):
        return self.__ABBREV
    
    
    def getLatexRapresentation(self):
        res = "-" if self.negated else ""
        denominatorElements = [child for child in self.children if isinstance(child, Pow) and child.children[1].negated]
        numeratorElements = [child for child in self.children if child not in denominatorElements]
        numerator = "\\cdot ".join([child.getLatexRapresentation() for child in numeratorElements])
        if len(denominatorElements) == 0:
            return res +numerator
        return res + "\\frac{" + numerator + "}{" + "\\cdot ".join([child.getLatexRapresentation(True) for child in denominatorElements]) + "}"
    
    @BaseLuppExpr.baseSimpl
    def simplify(self):
        children = []
        cumulatedFactor = Rational(1)
        sameBaseElements = {}

        # Calcolo il segno finale del prodotto
        negation = reduce(lambda res, child: res != child.negated, self.children, self.negated)
        self.children = [child.copy_with(negated = False) for child in self.children]

        for factor in self.children:
            # Se uno dei fattori è un prodotto, aggiungi i suoi figli
            if isinstance(factor, Mult):
                children.extend(factor.children)

            # Se uno dei fattori è un razionale, lo aggiungo al prodotto cumulato
            elif isinstance(factor, Rational):
                cumulatedFactor *= factor

            # Se uno dei fattori è una potenza, aggiungo la base e l'esponente alla lista delle potenze
            elif isinstance(factor, Pow):
                if (base:=factor.children[0]) in sameBaseElements:
                    sameBaseElements[base].append(factor.children[1])
                else:
                    sameBaseElements[base] = [factor.children[1]]

            # Altrimenti aggiungo il fattore alla lista degli elementi
            else:
                if factor in sameBaseElements:
                    sameBaseElements[factor].append(Rational(1))
                else:
                    sameBaseElements[factor] = [Rational(1)]
        
        for element, exponents in sameBaseElements.items():
            exp = Add(exponents).simplify() if len(exponents) > 1 else exponents[0]
            # Se ci sono più elementi con la stessa base, aggiungo la rispettiva potenzas
            if isinstance(exp, Rational):
                if exp.isZero():
                    children.append(Rational(1))
                elif exp.isOne():
                    children.append(element)
                else:
                    children.append(Pow(element, exp))
            else:
                children.append(Pow(element, exp))

        # Se non abbiamo figli tutto è stato semplificato. Ritorna 1
        if len(children) == 0:
            return cumulatedFactor.copy_with(negated = negation)
        
        # Se il fattore cumulato è zero, ritorna zero
        if cumulatedFactor.isZero():
            return Rational(0)
        
        # Se il fattore cumulato non è uno, lo aggiungo alla lista dei fattori
        if not cumulatedFactor.isOne():
            # Se il fattore cumulato è -1, inverto la negazione del primo figlio
            if cumulatedFactor.copy_with(negated = False).isOne():
                children[0] = children[0].copy_with(negated = not children[0].negated)
            else:
                children.insert(0, cumulatedFactor)
        
        # Se abbiamo più di un figlio, ritorna un nuovo prodotto
        if len(children) > 1:
            return Mult(children, negation)
        
        # Se abbiamo un solo figlio, ritorna il figlio
        return children[0].copy_with(negated = negation)
    
    @BaseLuppExpr.baseExpansion
    def expand(self):
        result = self.children[0]

        for child in self.children[1:]:
            firstElToMultiply = [result]
            if isinstance(result, Add):
                firstElToMultiply = result.children

            secondElToMultiply = [child]
            if isinstance(child, Add):
                secondElToMultiply = child.children

            elementsInProd = []  
            for element in firstElToMultiply:
                for secondElement in secondElToMultiply:
                    elementsInProd.append(Mult([element, secondElement]))

            result = Add(elementsInProd) if len(elementsInProd) > 1 else elementsInProd[0]

        result = result.copy_with(negated = result.negated != self.negated)
        return result
        
    @BaseLuppExpr.baseDerive
    def derive(self, symbol):
        addends = []
        for i, child in enumerate(self.children):
            addends.append(Mult([child.derive(symbol)] + self.children[:i] + self.children[i+1:]))
        res = ""
        for addend in addends:
            res += addend.getLatexRapresentation() + " + "
    
        return Add(addends, self.negated).simplify()

    
class Pow(BaseLuppExpr):
    '''
    This class represents the Pow node of the expression.
    The Pow node is used to represent the power of a base to an exponent.
    '''

    __NODE_NAME = "Pow"
    __ABBREV = "P"

    def __init__(self, base: BaseLuppExpr, exponent: BaseLuppExpr, negated = False):
        '''
        This method initializes the Pow object.
        The method takes the following parameters:
        - base: the base of the power.
        - exponent: the exponent of the power.
        '''
        assert (base is not None), "base cannot be None"
        assert (exponent is not None), "exponent cannot be None"
        super().__init__(self.__NODE_NAME, [base, exponent], negated)

    def copy_with(self, base = None, exponent = None, negated = None):
        return Pow(
            base = self.children[0] if base is None else base,
            exponent = self.children[1] if exponent is None else exponent,
            negated = self.negated if negated is None else negated
        )

    def getPayload(self):
        return self.__ABBREV
    
    def getLatexRapresentation(self, notAsFraction = False): 
        result = "-" if self.negated else ""
        base_latex = self.children[0].getLatexRapresentation()
        exp = self.children[1].copy_with(negated = False)

        if isinstance(exp,Rational) and exp.numerator == 1 and exp.denominator != 1:
            sqare = "[" + str(exp.denominator) + "]" if exp.denominator != 2 else ""
            result += "\\sqrt"+sqare+"{" + base_latex + "}"
        else:
            if isinstance(exp,Rational) and exp.numerator == 1:
                result += base_latex
            else:
                exponent_latex = exp.getLatexRapresentation() 
                result += f"{base_latex}^{{{exponent_latex}}}"

        if notAsFraction or not self.children[1].negated:
            return result
        return f"\\frac{{1}}{{{result}}}" if not self.negated else f"-\\frac{{1}}{{{result[1:]}}}"
        
    
    @BaseLuppExpr.baseSimpl
    def simplify(self):
        if isinstance(base:=self.children[0], Rational):
            if base.isZero():
                return Rational(0)
            if base.isOne():
                return Rational(1, self.negated)
        if isinstance(exponent:=self.children[1], Rational):
            if exponent.isZero():
                return Rational(1, self.negated)
            if exponent.isOne():
                return self.children[0].copy_with(negated = self.negated != self.children[0].negated)
            
        if isinstance(base, Pow):
            return Pow(base.children[0], Mult([base.children[1], exponent]), self.negated).simplify()
            
        if base.negated:
            base = base.copy_with(negated = False)
            self.negated = not self.negated

        res = Pow(base, exponent, self.negated)
        return res
    
    
    def expand(self):
        if not isinstance(self.children[1], Rational):
            return Pow(self.children[0].expand(), self.children[1].expand(), self.negated)
            
        rationalExponent = self.children[1]
        newBase = self.children[0].expand()
        
        if abs(rationalExponent.numerator) != 1:
            newBase = Mult([newBase for _ in range(abs(rationalExponent.numerator))])

        oldExponentSignNegated = (abs(rationalExponent.numerator) / rationalExponent.numerator) == -1
        oldExponentSignNegated = oldExponentSignNegated != rationalExponent.negated

        exp = Rational(1, rationalExponent.denominator, oldExponentSignNegated)

        if exp.isOne():
            return newBase.copy_with(negated = self.negated)
        
        return Pow(newBase, Rational(1, rationalExponent.denominator, oldExponentSignNegated), self.negated)

    @BaseLuppExpr.baseDerive
    def derive(self, symbol):
        assert isinstance(self.children[1], Rational), "Cannot derive a power with a non rational exponent"
        return Mult([self.children[1], Pow(self.children[0], Add([self.children[1], Rational(-1)])), self.children[0].derive(symbol)]).simplify()




    