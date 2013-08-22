// Copyright (C) 2011-2013 Andy Balaam and The Pepper Developers
// Released under the MIT License.  See the file COPYING.txt for details.

// Inspired in places by:
// http://www.antlr.org/grammar/1200715779785/Python.g
// Thanks to Terence Parr and Loring Craymer

options
{
    language = "Python";
}

class PepperLexer extends Lexer;

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



protected TRIPLEDOUBLEQUOTE :
    '"' '"' '"'
;

protected DOUBLEQUOTE : // TODO: single quoted strings
      '"'
;

protected DOUBLEQUOTESTRING :
    DOUBLEQUOTE!
    ( ~( '"' ) )*
    DOUBLEQUOTE!
;

protected TRIPLEDOUBLEQUOTESTRING :
    TRIPLEDOUBLEQUOTE!
    ( options {greedy=false;} : . )*
    TRIPLEDOUBLEQUOTE!
;

STRING :
    (
        // Pick triple-quoted string whenever we see 3 quotes,
        // rather than one empty double-quoted string followed by
        // the start of another.
        options {generateAmbigWarnings=false;} :
              TRIPLEDOUBLEQUOTESTRING
            | DOUBLEQUOTESTRING
    )
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
MINUS : '-' ;
TIMES : '*' ;

PLUSEQUALS : "+=" ;

GT : '>' ;

COLON : ':';

EQUALS : '=';

class PepperParser extends Parser;

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
    | modification
    | functionDefinition
    | classDefinition
    | interfaceDefinition
    | forStatement
    | importStatement
;

classStatement :
    statement
    | initFunctionDefinition
;

interfaceStatement :
    interfaceFunctionDefinition
;

initialisationOrExpression :
    expression ( SYMBOL EQUALS^ expression )? NEWLINE!
;

modification :
    SYMBOL PLUSEQUALS^ expression NEWLINE!
;

functionDefinition :
    "def"^ expression SYMBOL typedArgumentsList suite NEWLINE!
;

interfaceFunctionDefinition :
    "def"^ expression SYMBOL typedArgumentsList NEWLINE!
;

initFunctionDefinition :
    "def_init"^ typedArgumentsList initFunctionSuite NEWLINE!
;

classDefinition :
    "class"^ SYMBOL classSuite NEWLINE!
;

interfaceDefinition :
    "interface"^ SYMBOL interfaceSuite NEWLINE!
;

forStatement :
    "for"^ expression SYMBOL "in"! expression suite NEWLINE!
;

importStatement :
    "import"^ SYMBOL NEWLINE!
;

noCommaExpression :
    LPAREN! expression RPAREN! | calcExpression
;

expression :
    LPAREN! expression RPAREN! | commaExpression
;

commaExpression :
    calcExpression ( COMMA^ calcExpression ( COMMA! calcExpression )* )?
;

calcExpression :
    simpleExpression ( ( PLUS^ | MINUS^ | TIMES^ | GT^ ) noCommaExpression )?
;

typedArgumentsList :
    LPAREN^
    ( noCommaExpression SYMBOL ( COMMA noCommaExpression SYMBOL )* )?
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
    | quotedCode
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

quotedCode :
    "quote"^ suite
;

argumentsList:
    ( noCommaExpression ( COMMA noCommaExpression )* )?
;

suite :
    COLON^
    ( NEWLINE! )+
    INDENT!
    ( NEWLINE! )*
    ( statement ( NEWLINE! )* | returnStatement ( NEWLINE! )* )+
    DEDENT!
;

classSuite :
    COLON^
    ( NEWLINE! )+
    INDENT!
    ( NEWLINE! )*
    ( classStatement ( NEWLINE! )* )+
    DEDENT!
;

interfaceSuite :
    COLON^
    ( NEWLINE! )+
    INDENT!
    ( NEWLINE! )*
    ( interfaceStatement ( NEWLINE! )* )+
    DEDENT!
;

initFunctionSuite :
    COLON^
    ( NEWLINE! )+
    INDENT!
    ( NEWLINE! )*
    (
          ( varStatement ( statement ( NEWLINE! )* )* )
        | ( statement ( NEWLINE! )* )+
    )
    DEDENT!
;

varSuite :
    COLON^
    ( NEWLINE! )+
    INDENT!
    ( NEWLINE! )*
    ( initialisation ( NEWLINE! )* )+
    DEDENT!
;

initialisation :
    expression SYMBOL EQUALS^ expression NEWLINE!
;

varStatement :
    "var"^ varSuite NEWLINE!
;

returnStatement :
    "return"^ expression NEWLINE!
;

{
from libpepper.vals.all_values import *
}
class PepperTreeWalker extends TreeParser;

statement returns [r]
    : e=expression { r = e }
    | i=initialisation { r = i }
    | m=modification { r = m }
    | f=functionDefinition { r = f }
    | c=classDefinition { r = c }
    | n=interfaceDefinition { r = n }
    | f=forStatement { r = f }
    | i=importStatement { r = i }
;

classStatement returns [r]
    : s=statement { r = s }
    | f=initFunctionDefinition { r = f }
;

interfaceStatement returns [r]
    : f=interfaceFunctionDefinition { r = f }
;

expression returns [r]
    : s=symbol { r = s }
    | i:INT    { r = PepInt(    i.getText() ) }
    | d:FLOAT  { r = PepFloat(  d.getText() ) }
    | t:STRING { r = PepString( t.getText() ) }
    | a=arraylookup { r = a }
    | i=ifExpression { r = i }
    | #(PLUS e1=expression e2=expression) { r = PepPlus( e1, e2 ) }
    | #(MINUS e1=expression e2=expression) { r = PepMinus( e1, e2 ) }
    | #(TIMES e1=expression e2=expression) { r = PepTimes( e1, e2 ) }
    | #(GT e1=expression e2=expression) { r = PepGreaterThan( e1, e2 ) }
    | f=functionCall { r = f }
    | q=quotedCode { r = q }
    | t=tuple { r = t }
;

initialisation returns [r]
    : #(EQUALS t=expression s=symbol v=expression)
        { r = PepInit( t, s, v ) }
;

modification returns [r]
    : #(PLUSEQUALS s=symbol v=expression)
        { r = PepModification( s, v ) }
;

functionDefinition returns [r]
    : #("def" t=expression n=symbol a=typedArgumentsList s=suite)
        { r = PepDef( t, n, a, s ) }
;

interfaceFunctionDefinition returns [r]
    : #("def" t=expression n=symbol a=typedArgumentsList)
        { r = PepInterfaceDef( t, n, a ) }
;

initFunctionDefinition returns [r]
    : #("def_init" a=typedArgumentsList s=initFunctionSuite)
        { r = PepDefInit( a, s ) }
;

classDefinition returns [r]
    : #("class" n=symbol s=classSuite)
        { r = PepClass( n, (), s ) }
;

interfaceDefinition returns [r]
    : #("interface" n=symbol s=interfaceSuite)
        { r = PepInterface( n, (), s ) }
;

forStatement returns [r]
    : #("for" t=expression v=symbol i=expression s=suite)
        { r = PepFor( t, v, i, s ) }
;

importStatement returns [r]
    : #("import" m:SYMBOL) { r = PepImport( m.getText() ) }
;

symbol returns [r]
    : f:SYMBOL { r = PepSymbol( f.getText() ) }
;

arraylookup returns [r]
    : #(LSQUBR arr=symbol idx=expression)
        { r = PepArrayLookup( arr, idx ) }
;

ifExpression returns [r]
    : #("if" pred=expression s=suite es=elseExpression )
        { r = PepIf( pred, s, es ) }
;

elseExpression returns [r]
    { r = None }
    : ( "else" s=suite { r = s } )?
;

quotedCode returns [r]
    : #("quote" s=suite ) { r = PepQuote( s ) }
;

tuple returns [r]
    : t=tupleContents { r = PepTuple( t ) }
;

tupleContents returns [r]
    : #(COMMA
        e=expression { r = (e,) }
        ( e=expression { r += (e,) } )*
    )
;

functionCall returns [r]
    : #(LPAREN f=symbol a=argumentsList) { r = PepFunctionCall( f, a ) }
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

interfaceSuite returns [r]
    : #(COLON s=interfaceStatementsList) { r = s }
;

initFunctionSuite returns [r]
    : #(COLON s=initFunctionStatementsList) { r = s }
;

varSuite returns [r]
    : #(COLON s=initialisationsList) { r = s }
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

interfaceStatementsList returns [r]
    { r = () }
    : s=interfaceStatement { r = (s,) }
      ( s=interfaceStatement { r += (s,) } )*
;

initFunctionStatementsList returns [r]
    { r = () }
    : (
          v=varStatement { r = (v,) }
        | s=statement { r = (s,) }
      )
      ( s=statement { r += (s,) } )*
;

initialisationsList returns [r]
    { r = () }
    : i=initialisation { r = (i,) }
      ( i=initialisation { r += (i,) } )*
;


varStatement returns [r]
    : #("var" s=varSuite ) { r = PepVar( s ) }
;

statementOrReturnStatement returns [r]
    : s=statement { r = s }
    | #("return" e=expression) { r = PepReturn( e ) }
;

