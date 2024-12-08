

from src.utils.LuppoloLogger import LuppoloLogger

from src.expression.BaseLuppExpr import BaseLuppExpr
from src.expression.leaf import Rational, Symbol
from src.expression.nodes import Pow

from src.interpreter.LuppoloInterpException import LuppoloInterpException

# TODO: Metti a posto secondo la documentazione

class LuppoloLibraryFunctions:
    @staticmethod
    def Expand(expr):
        '''
        This function expands the expression passed as argument and returns it.
        '''
        if not isinstance(expr, BaseLuppExpr):
            LuppLoggerWitExc.logError("Argument passed to Expand function is not an expression.")
        return expr.expand()
    
    @staticmethod
    def Substitute(expr, match, subst):
        '''
        This function substitutes all the match inside the expr expression with the subst 
        in the expression passed as argument and return it.
        '''
        exprEle = [expr, match, subst]
        if not all([isinstance(el, BaseLuppExpr) for el in exprEle]):
            LuppLoggerWitExc.logError("Arguments passed to Substitute function are not all expressions.")
        return expr.substitute(match, subst)

    @staticmethod
    def Eval(expr, rat):
        '''
        This function evaluates the expression passed as argument substituting the only symbol
        present in the expression with the rational passed as argument.
        An error is raised if the expression has more than one symbol or no symbols.
        '''

        if not isinstance(expr, BaseLuppExpr):
            LuppLoggerWitExc.logError("Argument expr passed to Eval function is not an expression.")
        if not isinstance(rat, Rational):
            LuppLoggerWitExc.logError("Argument rat passed to Eval function is not a rational.")

        symbols = expr.findInnerElementsOfType(Symbol)
        print("Founded symbols: ", symbols)
        if len(symbols) > 1:
            LuppLoggerWitExc.logError("The expression has more than one symbol. Cannot apply eval.")
        if len(symbols) == 0:
            LuppLoggerWitExc.logError("The expression has no symbols. Cannot apply eval.")
        
        sym : Symbol = symbols.pop()
        return expr.substitute(sym, rat)

    @staticmethod
    def SimplDerive(expr, sym):
        '''
        This function simplifies the derivative of the expression passed as argument with respect 
        to the symbol passed as argument.
        An error is raised if the expression contains power with non-rational exponents.
         '''

        if not isinstance(expr, BaseLuppExpr):
            LuppLoggerWitExc.logError("Argument expr passed to SimplDerive function is not an expression.")
        if not isinstance(sym, Symbol):
            LuppLoggerWitExc.logError("Argument sym passed to SimplDerive function is not a symbol.")
        
        pows = expr.findInnerElementsOfType(Pow)
        
        # Controllo che non ci siano potenze con esponenti non razionali
        if any([not isinstance(pow.children[1], Rational) for pow in pows]):
            LuppLoggerWitExc.logError("Cannot derive expression containing power with non-rational exponents.")
        

        return expr.derive(sym).simplify()

    @staticmethod
    def DerivePolynomial(expr,sym):
        '''
        This function derives the polynomial passed as argument with respect to the symbol passed as argument.
        An error is raised if the polynomial has more than one variable or no variables or if the symbol 
        passed is not the variable of the polynomial.
        '''

        if not isinstance(expr, BaseLuppExpr):
            LuppLoggerWitExc.logError("Argument expr passed to DerivePolynomial function is not an expression.")
        
        if not isinstance(sym, Symbol):
            LuppLoggerWitExc.logError("Argument sym passed to DerivePolynomial function is not a symbol.")

        expandedExpr = expr.expand()
        exprVariables = expandedExpr.findInnerElementsOfType(Symbol)

        if len(exprVariables) > 1:
            LuppLoggerWitExc.logError("Cannot derive polynomial with more than one variable.")

        if len(exprVariables) == 0:
            LuppLoggerWitExc.logError("Cannot derive polynomial with no variables.")
        
        if exprVariables.pop() != sym:
            LuppLoggerWitExc.logError("The symbol passed as argument is not the variable of the polynomial.")

        return LuppoloLibraryFunctions.SimplDerive(expr.expand(), sym)
    


    availableFunctions = {
        "Expand": Expand,
        "Substitute": Substitute,
        "Eval": Eval,
        "SimplDerive": SimplDerive,
        "DerivePolynomial": DerivePolynomial
    }


class LuppLoggerWitExc(LuppoloLogger):
    @staticmethod
    def logError(message):
        super().logError(message)
        raise LuppoloInterpException()