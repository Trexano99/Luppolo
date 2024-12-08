Main(){
    Expr = 2*(x+1)*a^(x+1)
    Match = x+1
    Subst = y
    Result = Substitute(Expr, Match, Subst) 
    if (Result == ResultExpected()){
        return 1
    }
    return 0
}

ResultExpected(){
    return 2*y*a^y
}