
import LexedParser
import LexedLexer

from antlr import TokenStream

class EeyoreTokenStreamFromFile( TokenStream ):
    def __init__( self, fl ):
        self.lexed_parser = LexedParser.Parser(
            LexedLexer.Lexer( fl ) )

    def nextToken( self ):
        return self.lexed_parser.line()

    def __iter__( self ):
        return self

    def next( self ):
        nxt = self.nextToken()
        if nxt is None:
            raise StopIteration()
        return nxt

