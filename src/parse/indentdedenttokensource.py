
# Inspired in places by:
# http://www.antlr.org/depot/examples-v3/java/python/PythonTokenSource.java
# Thanks to Terence Parr and Loring Craymer

from antlr import TokenStream

import EeyoreLexer
from iterablefromtokenstream import IterableFromTokenStream

class IndentDedentTokenSource( TokenStream, IterableFromTokenStream ):
    def __init__( self, base_source ):
        self.base_source = base_source
        self.waiting_token_stack = []

    def nextToken( self ):
        if len( self.waiting_token_stack ) > 0:
            return self.waiting_token_stack.pop()

        tok = self.base_source.nextToken()
        if tok.getType() == EeyoreLexer.LEADINGSP:
            next_tok = self.base_source.nextToken()
            self.waiting_token_stack.append( next_tok )
            if next_tok.getType() == EeyoreLexer.NEWLINE:
                # If we a line containing only a comment or nothing
                # but whitespace, just emit the newline
                return self.nextToken()
            else:
                return self.nextToken() # TODO: emit an indent or dedent
        else:
            return tok


