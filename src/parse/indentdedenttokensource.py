
from antlr import TokenStream

from iterablefromtokenstream import IterableFromTokenStream

class IndentDedentTokenSource( TokenStream, IterableFromTokenStream ):
    def __init__( self, base_source ):
        self.base_source = base_source

    def nextToken( self ):
        return self.base_source.nextToken()


