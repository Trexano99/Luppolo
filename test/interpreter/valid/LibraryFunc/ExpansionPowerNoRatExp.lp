Main(){
    PowerToExpand = (3*(x+1))^((x+1)*x)
    ExpandedPower = Expand(PowerToExpand)
    if (ExpandedPower == ResultExpected()){
        return 1
    }
    return 0
}

ResultExpected(){
    return (3*x+3)^(x^2+x)
}