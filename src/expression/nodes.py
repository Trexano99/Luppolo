
from abc import ABC, abstractmethod
from functools import reduce

from src.expression.BaseLuppExpr import BaseLuppExpr
from src.expression.leaf import Rational

class Add(BaseLuppExpr):

    __NODE_NAME = "Add"
    __ABBREV = "S"

    def __init__(self, addends: list, negated = False):
        assert (addends is not None), "addends cannot be None"
        assert (len(addends) > 1), "addends must be at least two elements"
        super().__init__(self.__NODE_NAME, addends, negated)

    def getPayload(self):
        return self.__ABBREV
    
    def getLatexRapresentation(self):
        #Set sign if sum is all negated
        sign = "-" if self.negated else ""
        core = self.children[0].getLatexRapresentation()
        for child in self.children[1:]:
            # If the child is negated, add a minus sign, otherwise add a plus sign
            core += ("" if child.negated else "+") + child.getLatexRapresentation()
        # If the parent is a multiplication, add brackets
        if self.parent is not None and (isinstance(self.parent, Mult) or isinstance(self.parent, Pow)):
            core = f"\\left({core}\\right)"
        return sign + core
    
    @BaseLuppExpr.baseSimpl
    def simplify(self):

        children = []
        cumulatedSum = Rational(0)
        multiplicativeFactors = {}
        for addend in self.children:
            # Se uno degli addendi è una somma, aggiungi i suoi addendi
            if isinstance(addend, Add):
                children.extend(addend.children)
            # Se uno degli addendi è un razionale, aggiungilo alla somma cumulata
            elif isinstance(addend, Rational):
                cumulatedSum += addend
            # Se uno degli addendi è un prodotto con un razionale davanti, 
            # aggiungi il prodotto alla lista dei fattori moltiplicativi
            else:
                rationalPart = Rational(1)
                if isinstance(addend, Mult) and isinstance(addend.children[0], Rational):
                    rationalPart = addend.children[0]
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
            if rational.isOne():
                children.append(factor)
            else:
                children.append(Mult([rational, factor], addend.negated).simplify())
        
        # Se la lista degli addendi è vuota, ritorna zero
        if len(children) == 0:
            return Rational(0)
        
        # Se c'è più di un addendo, ritorna un nuovo addendo
        if len(children) > 1:
            return Add(children, self.negated)
        
        # Se c'è un solo addendo, ritorna l'unico addendo
        if self.negated: children[0].inverseNegation()
        return children[0]

class Mult(BaseLuppExpr):

    __NODE_NAME = "Mul"
    __ABBREV = "M"

    def __init__(self, factors: list, negated = False):
        assert (factors is not None), "factors cannot be None"
        assert (len(factors) > 1), "factors must be at least two elements"
        super().__init__(self.__NODE_NAME, factors, negated)

    def getPayload(self):
        return self.__ABBREV
    
    
    def getLatexRapresentation(self):
         res = "-" if self.negated else ""
         return res + "\\cdot ".join([child.getLatexRapresentation() for child in self.children])
    
    @BaseLuppExpr.baseSimpl
    def simplify(self):
        children = []
        cumulatedFactor = Rational(1)
        sameBaseElements = {}
        sameBasePow = {}
        for factor in self.children:
            # Se uno dei fattori è un prodotto, aggiungi i suoi figli
            if isinstance(factor, Mult):
                children.extend(factor.children)

            # Se uno dei fattori è un razionale, lo aggiungo al prodotto cumulato
            elif isinstance(factor, Rational):
                cumulatedFactor *= factor

            # Se uno dei fattori è una potenza, aggiungo la base e l'esponente alla lista delle potenze
            elif isinstance(factor, Pow):
                if factor.children[0] in sameBasePow:
                    sameBasePow[factor.children[0]].append(factor.children[1])
                else:
                    sameBasePow[factor.children[0]] = [factor.children[1]]

            # Altrimenti aggiungo il fattore alla lista degli elementi
            else:
                if factor in sameBaseElements:
                    sameBaseElements[factor] += 1
                else:
                    sameBaseElements[factor] = 1
        
        # Se il prodotto dei fattori è zero, ritorna zero
        if cumulatedFactor.isZero():
            return Rational(0)
        # Se il prodotto dei fattori non è uno, aggiungilo alla lista degli elementi
        elif not cumulatedFactor.isOne():
            children.append(cumulatedFactor)
        
        for element, freq in sameBaseElements.items():
            # Se ci sono più elementi con la stessa base, aggiungo la rispettiva potenzas
            if freq > 1:
                children.append(Pow(element, Rational(freq)))
            #Altrimenti li aggiungo direttamente
            else:
                children.append(element)
        
        for base, exponents in sameBasePow.items():
            # Se ci sono più potenze con la stessa base, sommo gli esponenti
            if len(exponents) > 1:
                children.append(Pow(base, Add(exponents).simplify()))
            #Altrimenti li aggiungo direttamente
            else:
                children.append(Pow(base, exponents[0]))

        # Se non abbiamo figli tutto è stato semplificato. Ritorna 1
        if len(children) == 0:
            return Rational(1, self.negated)
        
        # Se abbiamo più di un figlio, ritorna un nuovo prodotto
        if len(children) > 1:
            return Mult(children, self.negated)
        
        # Se abbiamo un solo figlio, ritorna il figlio
        if self.negated: children[0].inverseNegation()
        return children[0]
    
    
class Pow(BaseLuppExpr):

    __NODE_NAME = "Pow"
    __ABBREV = "P"

    def __init__(self, base: BaseLuppExpr, exponent: BaseLuppExpr, negated = False):
        assert (base is not None), "base cannot be None"
        assert (exponent is not None), "exponent cannot be None"
        print("Initializing pow with base: ", base, " and exponent: ", exponent)
        super().__init__(self.__NODE_NAME, [base, exponent], negated)

    def getPayload(self):
        return self.__ABBREV
    
    def getLatexRapresentation(self):
        print("Printing latex representation of pow with base: ", self.children[0], " and exponent: ", self.children[1])  
        base_latex = self.children[0].getLatexRapresentation()
        exponent_latex = self.children[1].getLatexRapresentation()
        return ("-" if self.negated else "") + f"{base_latex}^{{{exponent_latex}}}"
    
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
                if self.negated: return self.children[0].inverseNegation()
                return self.children[0] 
            
        return Pow(base, exponent, self.negated)
    