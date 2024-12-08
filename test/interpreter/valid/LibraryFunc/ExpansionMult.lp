Main(){
    MultToExpand = x*(y+2)*(z+3)
    ExpandedMult = Expand(MultToExpand)
    if (ExpandedMult == ResultExpected()){
        return 1
    }
    return 0
}

ResultExpected(){
    return x*y*z + 3*x*y + 2*x*z + 6*x
}