
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
}

program :
    ( NEWLINE )*
    ( statement ( NEWLINE )+ )* EOF
;

statement :
      functionCall
    | importStatement
;

functionCall :
    expression
    (LPAREN^)
    (expression)?
    (COMMA! expression)*
    (RPAREN!)
;

expression :
      SYMBOL
    | INT
    | STRING
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
    | i=importStatement { r = i }
;

functionCall returns [r]
    { r = None }
    : #(LPAREN f=function a=arg) { r = EeyFunctionCall( f, (a,) ) }
;

function returns [r]
    { r = None }
    : f:SYMBOL { r = EeySymbol( f.getText() ) }
;

arg returns [r]
    { r = None }
    : s:SYMBOL { r = EeySymbol( s.getText() ) }
    | i:INT    { r = EeyInt(    i.getText() ) }
    | t:STRING { r = EeyString( t.getText() ) }
;

importStatement returns [r]
    : #("import" m:SYMBOL) { r = EeyImport( m.getText() ) }
;

