Main(){
    Expr = x+2*y
    Match = x
    Subst = y
    Result = Substitute(Expr, Match, Subst) 
    if (Result == ResultExpected()){
        return 1
    }
    return 0
}

ResultExpected(){
    return 3*y
}