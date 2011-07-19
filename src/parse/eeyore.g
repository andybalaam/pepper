
options
{
    language = "Python";
}

class EeyoreLexer extends Lexer;

options
{
    charVocabulary = '\0'..'\377';
    testLiterals = false;    // don't automatically test for literals
    k = 2;                   // two characters of lookahead
}

WHITESPACE :
    (
          ' '
        | '\t'
        | '\f'
    )
    { $setType(Token.SKIP); }
;

COMMENT :
    "#" (~('\n'|'\r'))*
    { $setType(Token.SKIP); }
;

protected DIGIT :
    '0'..'9'
;

INT :
    (DIGIT)+
;

protected QUOTE : // TODO: single quoted strings
      '"'
;

STRING :
    QUOTE!
    ( ~( '"') )*
    QUOTE!
;

LPAREN :
    '('
;

RPAREN :
    ')'
;

LSQUBR : "[" ;
RSQUBR : "]" ;

COMMA :
    ','
;

protected STARTSYMBOLCHAR :
    (
          'a'..'z'
        | 'A'..'Z'
        | '_'
    )
;

protected MIDSYMBOLCHAR :
    (
          'a'..'z'
        | 'A'..'Z'
        | '0'..'9'
        | '_'
    )
;

protected SYMBOL_EL :
    STARTSYMBOLCHAR ( MIDSYMBOLCHAR )*
;

SYMBOL :
    SYMBOL_EL ( "." SYMBOL_EL )*
;

NEWLINE :
      "\r\n"
    | '\r'
    | '\n'
        { $newline }
;


class EeyoreParser extends Parser;

options
{
    buildAST = true;
    k = 2;
}

program :
    ( NEWLINE )*
    ( statement ( NEWLINE )+ )* EOF
;

statement :
      expression
    | importStatement
;


expression :
      SYMBOL
    | INT
    | STRING
    | functionCall
    | arrayLookup
;


functionCall :
    SYMBOL
    (LPAREN^)
    (expression)?
    (COMMA! expression)*
    (RPAREN!)
;

arrayLookup :
    SYMBOL (LSQUBR^) expression (RSQUBR!)
;

importStatement :
    "import"^ SYMBOL
;

{
from libeeyore.values import *
from libeeyore.languagevalues import *
from libeeyore.functionvalues import *
}
class EeyoreTreeWalker extends TreeParser;

statement returns [r]
    { sc = None }
    : ( sc=statementContents )? NEWLINE { r = sc }
;

statementContents returns [r]
    : f=functionCall    { r = f }
    | e=expression      { r = e }
    | i=importStatement { r = i }
;

functionCall returns [r]
    : #(LPAREN f=symbol a=expression) { r = EeyFunctionCall( f, (a,) ) }
;

expression returns [r]
    : s=symbol { r = s }
    | i:INT    { r = EeyInt(    i.getText() ) }
    | t:STRING { r = EeyString( t.getText() ) }
    | a=arraylookup { r = a }
;

symbol returns [r]
    : f:SYMBOL { r = EeySymbol( f.getText() ) }
;

arraylookup returns [r]
    : #(LSQUBR arr=symbol idx=expression)
        { r = EeyArrayLookup( arr, idx ) }
;

importStatement returns [r]
    : #("import" m:SYMBOL) { r = EeyImport( m.getText() ) }
;

