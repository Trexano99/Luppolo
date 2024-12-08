Main(){
    Expr = (x+2)^(1/2)
    Result = DerivePolynomial(Expr, x)
    if (Result == ResultExpected()){
        return 1
    }
    return 0
}

ResultExpected(){
    return (1/2)*((x+2)^(-1/2))
}