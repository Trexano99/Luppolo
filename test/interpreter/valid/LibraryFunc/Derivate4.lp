Main(){
    Expr = (2*x+1)/x
    Result = DerivePolynomial(Expr, x)
    if (Result == ResultExpected()){
        return 1
    }
    return 0
}

ResultExpected(){
    return -1/x^2
}