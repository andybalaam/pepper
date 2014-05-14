// Copyright (C) 2011-2014 Andy Balaam and The Pepper Developers
// Released under the MIT License.  See the file COPYING.txt for details.

// Inspired in places by:
// http://www.antlr.org/grammar/1200715779785/Python.g
// Thanks to Terence Parr and Loring Craymer

options
{
    language = "Python";
}

class NewSyntaxPepperLexer extends Lexer;

options
{
    charVocabulary = '\0'..'\377';
    k = 2;
    defaultErrorHandler=false;
}

WHITESPACE :
    (
          ' ' | '\n'
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

protected DIGITS
    : ( DIGIT )+
;

protected INT
    : DIGITS
;

protected DOT : '.' ;

protected FLOAT
    : DOT DIGITS
    | DIGITS DOT ( DIGITS )?
;

INT_OR_DOT_OR_FLOAT
    : ( INT DOT ) => FLOAT { $setType(FLOAT) }
    | ( DOT )     => DOT   { $setType(DOT) }
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

LBRACE :
    '{'
;

RBRACE :
    '}'
;

PIPE :
    '|'
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

SEMICOLON: ';' ;

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
    STARTSYMBOLCHAR ( MIDSYMBOLCHAR )*
;


PLUS : '+' ;
MINUS : '-' ;
TIMES : '*' ;

PLUSEQUALS : "+=" ;

GT : '>' ;
LT : '<' ;

COLON : ':';

EQUALS : '=';
EQUALSEQUALS : "==";

class NewSyntaxPepperParser extends Parser;

options
{
    buildAST = true;
    k = 2;
    defaultErrorHandler=false;
}

program :
    ( statement )*
    EOF
;

statement
    : SEMICOLON
    | initialisationOrExpression
    | modification
    | functionDefinition
    | classDefinition
    | interfaceDefinition
    | whileStatement
    | importStatement
    | codeBlock
;

codeBlock :
    LBRACE^ ( codeBlockArgs ) ?
    (statement ) *
    RBRACE!
;

codeBlockArgs :
    PIPE^ SYMBOL PIPE!
;

classStatement :
    statement
    | initFunctionDefinition
;

interfaceStatement :
    interfaceFunctionDefinition
;

initialisationOrExpression :
    expression ( SYMBOL EQUALS^ expression )?
;

modification :
    SYMBOL PLUSEQUALS^ expression
;

functionDefinition :
    "def"^ expression SYMBOL typedArgumentsList suite
;

interfaceFunctionDefinition :
    "def"^ expression SYMBOL typedArgumentsList
;

initFunctionDefinition :
    "def_init"^ typedArgumentsList initFunctionSuite
;

classDefinition :
    "class"^ SYMBOL classSuite
;

interfaceDefinition :
    "interface"^ SYMBOL interfaceSuite
;

whileStatement :
    "while"^ expression suite
;

importStatement :
    "import"^ SYMBOL
;

noCommaExpression :
    LPAREN! expression RPAREN! | calcExpression
;

expression :
    LPAREN! expression RPAREN! | commaExpression
;

commaExpression :
    lookupExpression ( COMMA^ lookupExpression ( COMMA! lookupExpression )* )?
;

lookupExpression :
    calcExpression ( DOT^ calcExpression )?
;

calcExpression :
    simpleExpression ( ( EQUALSEQUALS^ | PLUS^ | MINUS^ | TIMES^ | GT^ | LT^ ) noCommaExpression )?
;

typedArgumentsList :
    LPAREN^
    ( noCommaExpression SYMBOL ( COMMA noCommaExpression SYMBOL )* )?
    RPAREN!
;

simpleExpression :
      INT
    | FLOAT
    | STRING
    | functionCallOrSymbol
    | arrayLookup
    | quotedCode
;

functionCallOrSymbol :
    SYMBOL
    (options {greedy=true;}:
        LPAREN^
        argumentsList
        RPAREN!
    )*
;

arrayLookup :
    SYMBOL LSQUBR^ expression RSQUBR!
;

quotedCode :
    "quote"^ suite
;

argumentsList:
    ( noCommaExpression ( COMMA noCommaExpression )* )?
;

protected suiteStart :
    ( NEWLINE! )+
    INDENT!
    ( NEWLINE! )*
;

protected suiteEnd :
    DEDENT!
;

suite :
    COLON^
    suiteStart
    ( statement ( NEWLINE! )* | returnStatement ( NEWLINE! )* )+
    suiteEnd
;

classSuite :
    COLON^
    suiteStart
    ( classStatement ( NEWLINE! )* )+
    suiteEnd
;

interfaceSuite :
    COLON^
    suiteStart
    ( interfaceStatement ( NEWLINE! )* )+
    suiteEnd
;

initFunctionSuite :
    COLON^
    suiteStart
    (
          ( varStatement ( statement ( NEWLINE! )* )* )
        | ( statement ( NEWLINE! )* )+
    )
    suiteEnd
;

varSuite :
    COLON^
    suiteStart
    ( initialisation ( NEWLINE! )* )+
    suiteEnd
;

initialisation :
    expression SYMBOL EQUALS^ expression
;

varStatement :
    "var"^ varSuite
;

returnStatement :
    "return"^ expression
;

{
from libpepper.vals.all_values import *
}
class NewSyntaxPepperTreeWalker extends TreeParser;

statement returns [r]
    : e=expression { r = e }
    | i=initialisation { r = i }
    | m=modification { r = m }
    | f=functionDefinition { r = f }
    | c=classDefinition { r = c }
    | n=interfaceDefinition { r = n }
    | w=whileStatement { r = w }
    | i=importStatement { r = i }
    | c=codeBlock { r = c }
;

codeBlock returns [r]
    : #(LBRACE a=codeBlockArgs s=statementsList) { r = PepCodeBlock(a, s) }
;

codeBlockArgs returns [r]
    : #(PIPE s=symbol) { r = (s,) }  // TODO: list of args, with types
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
    | #(PLUS e1=expression e2=expression) { r = PepPlus( e1, e2 ) }
    | #(MINUS e1=expression e2=expression) { r = PepMinus( e1, e2 ) }
    | #(TIMES e1=expression e2=expression) { r = PepTimes( e1, e2 ) }
    | #(GT e1=expression e2=expression) { r = PepGreaterThan( e1, e2 ) }
    | #(LT e1=expression e2=expression) { r = PepLessThan( e1, e2 ) }
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

whileStatement returns [r]
    : #("while" e=expression s=suite)
        { r = PepWhile( e, s ) }
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

