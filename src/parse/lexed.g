
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
}

protected DIGIT : '0'..'9';

COLON : ':' { $setType(Token.SKIP); } ;

SPACES : ( ' ' )+ { $setType(Token.SKIP); } ;

NEWLINE : '\n' { $newline; $setType(Token.SKIP); };

NUMBER : ( DIGIT )+ ;

SYMBOL : ( 'A'..'Z' )+ ;

CONTENT : '(' ( ~( ')' ) )* ')';


class LexedParser extends Parser;

line:
    linenum:NUMBER COLON colnum:NUMBER SPACES
    symbol:SYMBOL ( content:CONTENT )? NEWLINE
    {
        from antlr import CommonToken
        import EeyoreParser
        t = CommonToken()
        if content is not None:
            t.setText( content.getText()[1:-1] )
        t.setType( EeyoreParser._tokenNames.index( symbol.getText() ) )
        t.setLine( int( linenum.getText() ) )
        t.setColumn( int( colnum.getText() ) )
        self.eeytkns.append( t )
    }
;

program returns [self.eeytkns] { self.eeytkns = [] } :
    (line)+
;

