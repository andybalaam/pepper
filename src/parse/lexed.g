
options
{
    language = "Python";
}

class LexedLexer extends Lexer;

options
{
    charVocabulary = '\0'..'\377';
    testLiterals = false;    // don't automatically test for literals
    k = 2;
    defaultErrorHandler=false;
}

protected DIGIT : '0'..'9';

COLON : ':' ;

SPACES : ( ' ' )+ ;

NEWLINE : '\n' { $newline; };

NUMBER : ( DIGIT )+ ;

SYMBOL : ( 'A'..'Z' )+ ;

QUOTED_LITERAL  : '"' ( 'a' .. 'z' | '_' )+ '"' ;

CONTENT : '(' ( ~( ')' ) )* ')';


class LexedParser extends Parser;

options
{
    defaultErrorHandler=false;
}

protected tokenName returns [t]:
    (
        s:SYMBOL         { t=s }
      | l:QUOTED_LITERAL { t=l }
    )
;

line returns [t]:
    linenum:NUMBER COLON colnum:NUMBER SPACES
    symbol=tokenName ( content:CONTENT )? NEWLINE
    {
        from antlr import CommonToken
        import EeyoreParser
        t = CommonToken(
            type = EeyoreParser._tokenNames.index( symbol.getText() ) )
        if content is not None:
            t.setText( content.getText()[1:-1] )
        t.setLine( int( linenum.getText() ) )
        t.setColumn( int( colnum.getText() ) )
    }
;
exception // for rule
    catch [antlr.RecognitionException ex] {
        return None
    }

