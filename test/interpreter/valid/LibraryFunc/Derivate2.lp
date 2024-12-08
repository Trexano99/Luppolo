Main(){
    Expr = x^3
    Result = DerivePolynomial(Expr, x)
    if (Result == ResultExpected()){
        return 1
    }
    return 0
}

ResultExpected(){
    return 3*x^2
}