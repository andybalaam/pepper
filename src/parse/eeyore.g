
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

protected DIGITS
    : ( DIGIT )+
;

protected INT
    : DIGITS
;

protected FLOAT
    : '.' DIGITS
    | DIGITS '.' ( DIGITS )?
;

INT_OR_FLOAT
    : ( INT '.' ) => FLOAT { $setType(FLOAT) }
    | ( '.' )     => FLOAT { $setType(FLOAT) }
    | INT                  { $setType(INT) }
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
    | functionDefinition
    | importStatement
;

initialisationOrExpression :
    expression ( SYMBOL EQUALS^ expression )?
;

functionDefinition :
    "def"^ expression SYMBOL typedArgumentsList COLON suite
;

importStatement :
    "import"^ SYMBOL
;

expression :
    simpleExpression ( ( PLUS^ | GT^ ) expression )?
;

typedArgumentsList :
    LPAREN^
    ( expression SYMBOL ( COMMA expression SYMBOL )* )?
    RPAREN!
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
    argumentsList
    RPAREN!
;

arrayLookup :
    SYMBOL LSQUBR^ expression RSQUBR!
;

ifExpression :
    "if"^ expression COLON suite
;

argumentsList:
    ( expression ( COMMA expression )* )?
;

suite :
    NEWLINE
    INDENT^
    ( ( statement | returnStatement ) NEWLINE )+
    DEDENT
;

returnStatement :
    "return"^ expression
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
    : e=expression { r = e }
    | i=initialisation { r = i }
    | f=functionDefinition { r = f }
    | i=importStatement { r = i }
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

initialisation returns [r]
    : #(EQUALS t=expression s=symbol v=expression) { r = EeyInit( t, s, v ) }
;

functionDefinition returns [r]
    : #("def" t=expression n=symbol a=typedArgumentsList COLON s=suite)
        { r = EeyDef( t, n, a, s ) }
;

importStatement returns [r]
    : #("import" m:SYMBOL) { r = EeyImport( m.getText() ) }
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

functionCall returns [r]
    : #(LPAREN f=symbol a=argumentsList) { r = EeyFunctionCall( f, a ) }
;

typedArgumentsList returns [r]
    { r = () }
    : #(LPAREN (
        e=expression s=symbol { r = ( (e,s), ) }
        ( COMMA e=expression s=symbol { r += ( (e,s), ) } )*
    )? )
;

suite returns [r]
    : #(INDENT NEWLINE s=statementsList DEDENT) { r = s }
;

argumentsList returns [r]
    { r = () }
    : (
        e=expression { r = (e,) }
        ( COMMA e=expression { r += (e,) } )*
    )?
;

statementsList returns [r]
    { r = () }
    : s=statementOrReturnStatement { r = (s,) }
      ( s=statementOrReturnStatement { r += (s,) } )*
;

statementOrReturnStatement returns [r]
    : s=statement { r = s }
    | #("return" e=expression) NEWLINE { r = EeyReturn( e ) }
;

