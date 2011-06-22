
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
        | (
              "\r\n"
            | '\r'
            | '\n'
          )
          { $newline }
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

INTLIT :
    (DIGIT)+
;

protected QUOTE : // TODO: single quoted strings
      '"'
;

//protected LINEFEED :
//    '\r'
//;
//
//protected CARRIAGERETURN :
//    '\n'
//;

//STRINGLIT : // TODO: escaped quotes within strings
//    QUOTE!
//    ( ~( '"'|'\r'|'\n' ) )* // Terminate string on quote or newline
//    ( QUOTE! | )            // Fail if there was no " at the end (i.e. newline)
//;

STRINGLIT :
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

SYMBOL :
    STARTSYMBOLCHAR(MIDSYMBOLCHAR)*
;


class EeyoreParser extends Parser;

options
{
    buildAST = true;
}

program :
    (statement)*
;

statement :
    functionCall
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
    | INTLIT
    | STRINGLIT
;

//operator :
//      SYMBOL
//    | expression
//;
//
//operand :
//            SYMBOL
//        | INTLIT
//        | STRINGLIT
//        | expression
//;


{
from libeeyore.values import *
from libeeyore.functionvalues import *
}
class EeyoreTreeWalker extends TreeParser;

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
    : s:SYMBOL     { r = EeySymbol( s.getText() ) }
    | i: INTLIT    { r = EeyInt(    i.getText() ) }
    | t: STRINGLIT { r = EeyString( t.getText() ) }
;

