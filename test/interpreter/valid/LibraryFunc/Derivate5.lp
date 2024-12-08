Main(){
    Expr = 1/4*x^4+x^3+3/2*x^2+x
    Result = DerivePolynomial(Expr, x)
    if (Result == ResultExpected()){
        return 1
    }
    return 0
}

ResultExpected(){
    return Expand((x+1)^3)
}