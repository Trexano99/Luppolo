

from src.utils.LuppoloLogger import LuppoloLogger

from src.expression.BaseLuppExpr import BaseLuppExpr
from src.expression.leaf import Rational, Symbol

class LuppoloLibraryFunctions:
    @staticmethod
    def Expand(expr):
        '''
        This function expands the expression passed as argument.
        '''
        if not isinstance(expr, BaseLuppExpr):
            LuppoloLogger.logError("Argument passed to Expand function is not an expression.")
            raise Exception("An error occurred during the execution of the Expand function.")
        return expr.expand()
    
    @staticmethod
    def Substitute(expr, match, subst):
        '''
        This function substitutes the match with the subst in the expression passed as argument.
        '''
        exprEle = [expr, match, subst]
        if not all([isinstance(el, BaseLuppExpr) for el in exprEle]):
            LuppoloLogger.logError("Arguments passed to Substitute function are not all expressions.")
            raise Exception("An error occurred during the execution of the Substitute function.")
        return expr.substitute(match, subst)

    @staticmethod
    def Eval(expr, rat):
        # TODO: Implement Eval functions

        if not isinstance(expr, BaseLuppExpr):
            LuppoloLogger.logError("Argument expr passed to Eval function is not an expression.")
            raise Exception("An error occurred during the execution of the Eval function.")
        if not isinstance(rat, Rational):
            LuppoloLogger.logError("Argument rat passed to Eval function is not a rational.")
            raise Exception("An error occurred during the execution of the Eval function.")

        symbols = expr.findInnerSymbols()
        print("Founded symbols: ", symbols)
        if len(symbols) > 1:
            LuppoloLogger.logError("The expression has more than one symbol. Cannot apply eval.")
            raise Exception("An error occurred during the execution of the Eval function.")
        if len(symbols) == 0:
            LuppoloLogger.logError("The expression has no symbols. Cannot apply eval.")
            raise Exception("An error occurred during the execution of the Eval function.")
        
        sym : Symbol = symbols.pop()
        return expr.substitute(sym, rat)

    @staticmethod
    def SimplDerive(expr, sym):
        '''
        This function simplifies the derivative of the expression passed as argument with respect to the symbol passed as argument.
        '''

        if not isinstance(expr, BaseLuppExpr):
            LuppoloLogger.logError("Argument expr passed to SimplDerive function is not an expression.")
            raise Exception("An error occurred during the execution of the SimplDerive function.")
        if not isinstance(sym, Symbol):
            LuppoloLogger.logError("Argument sym passed to SimplDerive function is not a symbol.")
            raise Exception("An error occurred during the execution of the SimplDerive function.")
        
        return expr.derive(sym).simplify()

    @staticmethod
    def DerivePolynomial(expr,sym):
        return LuppoloLibraryFunctions.SimplDerive(expr, sym)
    


    availableFunctions = {
        "Expand": Expand,
        "Substitute": Substitute,
        "Eval": Eval,
        "SimplDerive": SimplDerive,
        "DerivePolynomial": DerivePolynomial
    }