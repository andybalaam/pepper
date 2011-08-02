
# Inspired in places by:
# http://www.antlr.org/depot/examples-v3/java/python/PythonTokenSource.java
# Thanks to Terence Parr and Loring Craymer

from antlr import CommonToken
from antlr import TokenStream

import EeyoreLexer
from iterablefromtokenstream import IterableFromTokenStream
from libeeyore.usererrorexception import EeyUserErrorException

def _new_indent( tok ):
    ret = CommonToken()
    ret.setType( EeyoreLexer.INDENT )
    ret.setLine( tok.getLine() )
    ret.setColumn( tok.getColumn() )
    return ret

class IndentDedentTokenSource( TokenStream, IterableFromTokenStream ):
    def __init__( self, base_source ):
        self.base_source = base_source
        self.waiting_token_stack = []

    def nextToken( self ):
        if len( self.waiting_token_stack ) > 0:
            return self.waiting_token_stack.pop()

        tok = self.base_source.nextToken()
        if tok.getType() != EeyoreLexer.LEADINGSP:
            return tok

        return self.HandleLeadingSpace( tok )

    def HandleLeadingSpace( self, tok ):

        next_tok = self.base_source.nextToken()
        self.waiting_token_stack.append( next_tok )

        if next_tok.getType() in (
                EeyoreLexer.NEWLINE,
                EeyoreLexer.EOF,
                ):
            # If we find a line containing only a comment or nothing
            # but whitespace, just emit the newline (ignore the space)
            return self.nextToken()

        if ( len( tok.getText() ) % 4 ) == 0:
            self.waiting_token_stack.append( _new_indent( tok ) )
        else:
            raise EeyUserErrorException(
                "Indentation at the beginning of a line must be "
                + "4 spaces." )

        return self.nextToken() # TODO: emit an indent or dedent


