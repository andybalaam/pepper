
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
    defaultErrorHandler=false;
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
TIMES : '*' ;

GT : '>' ;

COLON : ':';

EQUALS : '=';

class EeyoreParser extends Parser;

options
{
    buildAST = true;
    k = 2;
    defaultErrorHandler=false;
}

program :
    ( NEWLINE! )*
    ( statement ( NEWLINE! )* )*
    EOF
;

statement :
      initialisationOrExpression
    | functionDefinition
    | classDefinition
    | importStatement
;

classStatement :
      initialisationOrExpression
    | functionDefinition
    | initFunctionDefinition
    | classDefinition
    | importStatement
;

initialisationOrExpression :
    expression ( SYMBOL EQUALS^ expression )? NEWLINE!
;

functionDefinition :
    "def"^ expression SYMBOL typedArgumentsList suite NEWLINE!
;

initFunctionDefinition :
    "def_init"^ typedArgumentsList suite NEWLINE!
;

classDefinition :
    "class"^ SYMBOL classSuite NEWLINE!
;

importStatement :
    "import"^ SYMBOL NEWLINE!
;

expression :
    simpleExpression ( ( PLUS^ | TIMES^ | GT^ ) expression )?
;

typedArgumentsList :
    LPAREN^
    ( expression SYMBOL ( COMMA expression SYMBOL )* )?
    RPAREN!
;

simpleExpression :
      SYMBOL
    | INT
    | FLOAT
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
    "if"^ expression suite ( NEWLINE! "else" suite )?
;

argumentsList:
    ( expression ( COMMA expression )* )?
;

suite :
    COLON^
    NEWLINE!
    INDENT!
    ( statement | returnStatement )+
    DEDENT!
;

classSuite :
    COLON^
    NEWLINE!
    INDENT!
    ( classStatement )+
    DEDENT!
;

returnStatement :
    "return"^ expression NEWLINE!
;

{
from libeeyore.values import *
from libeeyore.classvalues import *
from libeeyore.languagevalues import *
from libeeyore.functionvalues import *
}
class EeyoreTreeWalker extends TreeParser;

statement returns [r]
    : e=expression { r = e }
    | i=initialisation { r = i }
    | f=functionDefinition { r = f }
    | c=classDefinition { r = c }
    | i=importStatement { r = i }
;

classStatement returns [r]
    : e=expression { r = e }
    | i=initialisation { r = i }
    | f=functionDefinition { r = f }
    | f=initFunctionDefinition { r = f }
    | c=classDefinition { r = c }
    | i=importStatement { r = i }
;

expression returns [r]
    : s=symbol { r = s }
    | i:INT    { r = EeyInt(    i.getText() ) }
    | d:FLOAT  { r = EeyFloat(  d.getText() ) }
    | t:STRING { r = EeyString( t.getText() ) }
    | a=arraylookup { r = a }
    | i=ifExpression { r = i }
    | #(PLUS e1=expression e2=expression) { r = EeyPlus( e1, e2 ) }
    | #(TIMES e1=expression e2=expression) { r = EeyTimes( e1, e2 ) }
    | #(GT e1=expression e2=expression) { r = EeyGreaterThan( e1, e2 ) }
    | f=functionCall { r = f }
;

initialisation returns [r]
    : #(EQUALS t=expression s=symbol v=expression)
        { r = EeyInit( t, s, v ) }
;

functionDefinition returns [r]
    : #("def" t=expression n=symbol a=typedArgumentsList s=suite)
        { r = EeyDef( t, n, a, s ) }
;

initFunctionDefinition returns [r]
    : #("def_init" a=typedArgumentsList s=suite)
        { r = EeyDefInit( a, s ) }
;

classDefinition returns [r]
    : #("class" n=symbol s=classSuite)
        { r = EeyClass( n, (), s ) }
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
    : #("if" pred=expression s=suite es=elseExpression )
        { r = EeyIf( pred, s, es ) }
;

elseExpression returns [r]
    { r = None }
    : ( "else" s=suite { r = s } )?
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
    : #(COLON s=statementsList) { r = s }
;

classSuite returns [r]
    : #(COLON s=classStatementsList) { r = s }
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

classStatementsList returns [r]
    { r = () }
    : s=classStatement { r = (s,) }
      ( s=classStatement { r += (s,) } )*
;


statementOrReturnStatement returns [r]
    : s=statement { r = s }
    | #("return" e=expression) { r = EeyReturn( e ) }
;

