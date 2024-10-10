


grammar luppolo;

program
    : function+ EOF
    ;

function
    : ID LPAREN parameter_list? RPAREN block
    ;

parameter_list
    : ID (COMMA ID)*
    ;

block
    : LBRACE instruction* RBRACE
    ; 

instruction
    : 'foreach' ID 'in' expression block
    | 'if' condition block ('else' block)?
    | 'return' expression
    | 'while' condition block
    | 'repeat' expression block
    | ID EQUALS expression
    ;

expression
    : LPAREN expression RPAREN
    | (PLUS | MINUS) expression
    | NAT
    | SYM
    | ID
    | function_call
    | expression (POW | TIMES | DIV | PLUS | MINUS ) expression
    ;

condition
    : LPAREN condition RPAREN
    | expression (LEQ | LT | EQ | GT | GEQ) expression
    | NOT condition
    | condition (AND | OR) condition
    | 'true'
    | 'false'
    ;

function_call
    : ID LPAREN expression_list? RPAREN
    ;

expression_list
    : expression (COMMA expression)*
    ;

ID
    : [A-Z] [a-zA-Z]*
    ;

LPAREN
    : '('
    ;

RPAREN
    : ')'
    ;

LBRACE
    : '{'
    ;

RBRACE
    : '}'
    ;

EQUALS
    : '='
    ;

PLUS
    : '+'
    ;

MINUS
    : '-'
    ;

TIMES
    : '*'
    ;

DIV 
    : '/'
    ;   

POW
    : '^'
    ;   

LEQ
    : '<='
    ;  

LT  
    : '<'
    ;  

EQ
    : '=='
    ;

GT
    : '>'
    ;

GEQ 
    : '>='
    ;

AND
    : 'and'
    ;

OR
    : 'or'
    ;

NOT
    : '!'
    ;


NAT
    : [0-9]+
    ;

SYM
    : [a-z]
    ;

COMMA
    : ','
    ;

WS: [ \t\r\n]+ -> skip;