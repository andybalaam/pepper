
// Inspired in places by:
// http://www.antlr.org/grammar/1200715779785/Python.g
// Thanks to Terence Parr and Loring Craymer

options
{
    language = "Python";
}

class EeyoreLexer extends Lexer;

options
{
    charVocabulary = '\0'..'\377';
    k = 2;
}

tokens
{
    INDENT;
    DEDENT;
}

WHITESPACE : { self.getColumn() > 1 }?
    (
          ' '
    )
    { $setType(Token.SKIP); }
;

LEADINGSP: { self.getColumn() == 1 }
    ( ' ' )+
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

PLUS : '+' ;

GT : '>' ;

COLON : ':';

EQUALS : '=';

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
      initialisationOrExpression
    | importStatement
;

expression :
    simpleExpression ( ( PLUS^ | GT^ ) expression )?
;

simpleExpression :
      SYMBOL
    | INT
    | STRING
    | functionCall
    | arrayLookup
    | ifExpression
;


functionCall :
    SYMBOL
    LPAREN^
    ( expression )? ( COMMA! expression )*
    RPAREN!
;

arrayLookup :
    SYMBOL LSQUBR^ expression RSQUBR!
;

ifExpression :
    "if"^ expression COLON suite
;

suite :
    NEWLINE
    INDENT^
    ( statement NEWLINE )+
    DEDENT
;

initialisationOrExpression :
    expression ( SYMBOL EQUALS^ expression )?
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
    : e=expression      { r = e }
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
    | i=ifExpression { r = i }
    | #(PLUS e1=expression e2=expression) { r = EeyPlus( e1, e2 ) }
    | #(GT e1=expression e2=expression) { r = EeyGreaterThan( e1, e2 ) }
    | f=functionCall { r = f }
;

symbol returns [r]
    : f:SYMBOL { r = EeySymbol( f.getText() ) }
;

arraylookup returns [r]
    : #(LSQUBR arr=symbol idx=expression)
        { r = EeyArrayLookup( arr, idx ) }
;

ifExpression returns [r]
    : #("if" pred=expression COLON s=suite) { r = EeyIf( pred, s ) }
;

suite returns [r]
    : #(INDENT NEWLINE s=statement DEDENT) { r = ( s, ) }
;

importStatement returns [r]
    : #("import" m:SYMBOL) { r = EeyImport( m.getText() ) }
;

