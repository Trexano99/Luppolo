SquareTerms(Sum){
    Result = 0
    foreach Term in Sum {
        Result = Result + Term^2
    }
    return Result
}

Main(){
    TotVolte = 5
    N = 0

    repeat TotVolte{
        Result = 1+x
        repeat N{
            Result = Result + SquareTerms(Result)
        }
        FinalResult = Expand(Result)
        if !(FinalResult == ResultExpected(N)){
            return 0
        }
        N = N + 1
    }
    
    return 1
}

ResultExpected(N){
    if (N == 0){
        return 1+x
    }
    if (N == 1){
        return x+x^2+2
    }
    if (N == 2){
        return x+x^4+2*x^2+6
    }
    if (N == 3){
        return x+x^8+3*x^2+5*x^4+42
    }
    return x+x^16+4*x^2+14*x^4+18*x^8+1806
}