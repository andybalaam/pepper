
import antlr

import LexedParser
import LexedLexer

from iterablefromtokenstream import IterableFromTokenStream

class EeyoreTokenStreamFromFile( antlr.TokenStream, IterableFromTokenStream ):
    def __init__( self, fl ):
        self.lexed_parser = LexedParser.Parser(
            LexedLexer.Lexer( fl ) )

    def nextToken( self ):
        ln = self.lexed_parser.line()
        if ln is None:
            return antlr.CommonToken( type = antlr.Token.EOF_TYPE )
        else:
            return ln

