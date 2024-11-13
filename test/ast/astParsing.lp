/*
//TEST PROGRAM AND FUNC BASE
AFunction(){}
BFunction(AParam, Bparam){}
CFunction(AParam, Bparam, CParam){}


TestAllInstructions() { 
    AnId = 2
    foreach AnotherId in 2 {
        return 2
    }    
    if true {}
    if true {} else {}
    repeat AnExpressionId {}
    while true {}
    return AReturnValue
}
TestExpressions(A) {
    A = +1
    A = -1 
    A = --1
    A = 1 + 1
    A = 1 - 1
    A = 1 * 1
    A = 1 / 1
    A = 1 ^ 1
    A = 2
    A = B
    A = c
    A = (1+1)
}
TestConditions(){
    if true {}
    if false {}
    if !true {}
    if A < B {}
    if A <= B {}
    if A > B {}
    if A >= B {}
    if true or false {}
    if true and false {}
    if (true or false) and true {}
    if true or false and true {}
}
TestFuncCall(){
    A = AFuncNameID()
    B = ASecondFuncNameID(1)
    C = AThirdFuncNameId(AsecondFunc(d), AnID)
    D = LastFuncNameID(2/3^5, (2+3)*2)
}
/*
PowPrecedenceTests(){
    A = 2*3^2
    B = -3^2
    C = 5+2^3
    D = 2^3^2
}
ParenPrecedenceTests(){
    A = (2 * 3)^2 
    B = (-3)^2
    C = (5 + 2)^3
    D = (2^3)^2 
}
MulDivPrecedenceTests(){
    A = 2 + 3 * 4      
    B = 10 - 6 / 2    
    C = -3 * 4 + 5   
    D = 20 / -5 - 3  
}
AndOrPrecedenceTests(){
    if true or false and false {}
    if false and true or true {}
    if true and false or false {}
    if false or true and true {}  
}
NotAndOrPrecedenceTests(){
    if !true and false or true {}
    if true or !false and false {}
    if false and !true or true {}
    if !false or false and true {}  
}
SomeCompleteTests(){
    A = 1+2*3^4
    B = ((1+2)*3)^4
    C = 1+2*3^4+5
    D = 1+(2*3)^(4+5)
    E = -2^-1
}
MoreLongTests(){
    A = (2 + 3) * (4 - 1) ^ 2 / (5 - 3)  
    B = -5 + 3 * (2 ^ 2) / (1 + 1)  
    C = (6 - 4) * (3 + 2) ^ 2 / 5 + 1  
    D = 10 / 2 + 3 * (4 - 2 ^ 1)  
    E = (2 * 3) ^ 2 + (5 - 2) * (1 + 4)  
    F = -2 ^ 3 + 4 * (3 - (1 + 1))  
    G = (5 + 2) * 3 - (6 / 2) + 1  
}

*/

Main(){}