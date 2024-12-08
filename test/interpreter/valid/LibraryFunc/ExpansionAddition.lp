Main(){
    MultToExpand = x*(y+2)+z+(x+1)^2
    ExpandedMult = Expand(MultToExpand)
    if (ExpandedMult == ResultExpected()){
        return 1
    }
    return 0
}

ResultExpected(){
    return x*y + 4*x + + x^2 + z + 1
}