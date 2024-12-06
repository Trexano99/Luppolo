

from src.utils.LuppoloLogger import LuppoloLogger

from src.expression.BaseLuppExpr import BaseLuppExpr

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
    def Eval(expr):
        # TODO: Implement Eval functions
        raise NotImplementedError("Eval function is not implemented yet.")

    @staticmethod
    def SimplDerive(expr, sym):
        '''
        This function simplifies the derivative of the expression passed as argument with respect to the symbol passed as argument.
        '''
        exprSym = [expr, sym]
        if not all([isinstance(el, BaseLuppExpr) for el in exprSym]):
            LuppoloLogger.logError("Arguments passed to SimplDerive function are not all expressions.")
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