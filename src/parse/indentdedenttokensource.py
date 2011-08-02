
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

def _new_dedent( tok ):
    ret = CommonToken()
    ret.setType( EeyoreLexer.DEDENT )
    ret.setLine( tok.getLine() )
    ret.setColumn( tok.getColumn() )
    return ret


class IndentDedentTokenSource( TokenStream, IterableFromTokenStream ):
    def __init__( self, base_source ):
        self.base_source = base_source
        self.waiting_token_stack = []
        self.indents_stack = [0]
        self.last_newline = None

    def nextToken( self ):
        ret = self.GetNextToken()
        if ret.getType() == EeyoreLexer.NEWLINE:
            self.last_newline = ret
        return ret

    def GetNextToken( self ):
        if len( self.waiting_token_stack ) > 0:
            return self.waiting_token_stack.pop()

        tok = self.base_source.nextToken()

        if tok.getType() == EeyoreLexer.EOF:
            return self.HandleEof( tok )
        elif tok.getType() == EeyoreLexer.LEADINGSP:
            return self.HandleLeadingSpace( tok )
        else:
            return tok

    def HandleEof( self, tok ):
        self.waiting_token_stack.append( tok )
        while self.indents_stack[-1] > 0:
            tok = self.last_newline if self.last_newline is not None else tok
            self.waiting_token_stack.append( _new_dedent( tok ) )
            self.indents_stack.pop()
        return self.nextToken()

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

        indent_col = len( tok.getText() )
        if ( indent_col % 4 ) != 0:
            raise EeyUserErrorException(
                "Indentation at the beginning of a line must be "
                + "4 spaces." )

        if indent_col > self.indents_stack[-1]:
            self.indents_stack.append( indent_col )
            self.waiting_token_stack.append( _new_indent( tok ) )

        return self.nextToken() # TODO: emit an indent or dedent


