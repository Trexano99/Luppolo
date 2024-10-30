


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
    : <assoc=right> expression POW expression
    | LPAREN expression RPAREN
    | (PLUS | MINUS) expression
    | NAT
    | SYM
    | ID
    | function_call
    | expression (TIMES | DIV) expression
    | expression (PLUS | MINUS) expression
    ;

condition
    : LPAREN condition RPAREN
    | NOT condition
    | condition AND condition
    | condition OR condition
    | comparison_condition
    | TRUE | FALSE
    ;

comparison_condition
    : expression (LEQ | LT | EQ | GT | GEQ) expression
    ;


function_call
    : ID LPAREN expression_list? RPAREN
    ;

expression_list 
    : expression (COMMA expression)* 
    ;

// Lexer

// Parenthesis
LPAREN: '(';
RPAREN: ')';
LBRACE: '{';
RBRACE: '}';

// Operators
EQUALS: '=';    
PLUS: '+';
MINUS: '-';
TIMES: '*';
DIV: '/';
POW: '^';

// Comparison
LEQ: '<=';
LT: '<';
EQ: '==';
GT: '>';
GEQ: '>=';

// Logical
TRUE: 'true';
FALSE: 'false';
AND: 'and';
OR: 'or';
NOT: '!';

// Separators
COMMA: ',';

// Literals
ID: [A-Z] [a-zA-Z]*;
NAT: [0-9]+('.'[0-9]+)?;
SYM: [a-z];

// Whitespace
WS: [ \t\r\n]+ -> skip;

// Comments
LINE_COMMENT:  '//' ~[\r\n]* -> skip;
BLOCK_COMMENT: '/*' .*? '*/' -> skip;