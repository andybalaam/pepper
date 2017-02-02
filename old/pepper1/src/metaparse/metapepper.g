// Copyright (C) 2011-2013 Andy Balaam and The Pepper Developers
// Released under the MIT License.  See the file COPYING.txt for details.

// Inspired in places by:
// http://www.antlr.org/grammar/1200715779785/Python.g
// Thanks to Terence Parr and Loring Craymer

options
{
    language = "Python";
}

class MetaPepperLexer extends Lexer;

options
{
    charVocabulary='\u0000'..'\uFFFE';
}

// Ignore whitespace except at beginning of line
WHITESPACE : { self.getColumn() > 1 }?
    (
          ' '
    )
    { $setType(Token.SKIP); }
;

EQUALS : '=' ;
COLON  : ':' ;

protected LETTER : 'a'..'z' | 'A'..'Z' | '_' ;
protected DIGIT  : '0'..'9' ;
protected DIGITS : ( DIGIT )+ ;

INT : DIGITS ;

protected FLOAT
    : '.' DIGITS
    | DIGITS '.' ( DIGITS )?
;

protected NUMBER
    : ( INT '.' ) => FLOAT { $setType(FLOAT) }
    | ( '.' )     => FLOAT { $setType(FLOAT) }
    | INT                  { $setType(INT) }
;

SYMBOL : LETTER ( LETTER | DIGIT )* ;


class MetaPepperParser extends Parser;

protected expression : SYMBOL | INT;

protected type  : expression ;
protected name  : SYMBOL ;
protected value : expression ;

protected assignment : type name EQUALS value
    { print "assignment" }
;

protected block : function block_arg suite ;

program : assignment ;




