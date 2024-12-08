Main(){
    PowerToExpand = (x+1)^(-3/2)
    ExpandedResult = Expand(PowerToExpand)
    if (ExpandedResult == ResultExpected()){
        return 1
    }
    return 0
}

ResultExpected(){
    return (x^3+3*x^2+3*x+1)^(-1/2)
}