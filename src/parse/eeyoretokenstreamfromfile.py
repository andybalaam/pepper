
import LexedParser
import LexedLexer

import antlr

class EeyoreTokenStreamFromFile( antlr.TokenStream ):
    def __init__( self, fl ):
        self.lexed_parser = LexedParser.Parser(
            LexedLexer.Lexer( fl ) )

    def nextToken( self ):
        ln = self.lexed_parser.line()
        if ln is None:
            return antlr.CommonToken( type = antlr.Token.EOF_TYPE )
        else:
            return ln

    def __iter__( self ):
        return self

    def next( self ):
        nxt = self.nextToken()
        if nxt.getType() == antlr.Token.EOF_TYPE:
            raise StopIteration()
        return nxt

