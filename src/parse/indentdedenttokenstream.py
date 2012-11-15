# Copyright (C) 2011-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


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

def _new_newline( tok ):
    ret = CommonToken()
    ret.setType( EeyoreLexer.NEWLINE )
    ret.setLine( tok.getLine() )
    ret.setColumn( tok.getColumn() )
    return ret


class IndentDedentTokenStream( TokenStream, IterableFromTokenStream ):
    def __init__( self, base_source ):
        self.base_source = base_source
        self.waiting_token_stack = []
        self.indents_stack = [0]
        self.last_newline = None

    def nextToken( self ):
        ret = self.GetNextToken()
        if ret.getType() == EeyoreLexer.NEWLINE:
            self.last_newline = ret
        else:
            self.last_newline = None
        return ret


    def GetNextToken( self ):
        if len( self.waiting_token_stack ) > 0:
            return self.waiting_token_stack.pop()

        tok = self.base_source.nextToken()

        if tok.getType() == EeyoreLexer.EOF:
            # If we're at the end of the file generate some dedents
            return self.DedentToLeft( tok )
        elif tok.getType() == EeyoreLexer.LEADINGSP:
            # If we hit some leading spaces, generate indents or dedents
            return self.HandleLeadingSpace( tok )
        elif tok.getType() == EeyoreLexer.NEWLINE:
            return tok
        elif self.last_newline is not None:
            # If we are the beginning a new line but there is no leading
            # whitespace,we must dedent all the way to the left
            return self.DedentToLeft( tok )
        else:
            return tok


    def DedentToLeft( self, tok ):
        self.waiting_token_stack.append( tok )
        while self.indents_stack[-1] > 0:
            tok = self.last_newline if self.last_newline is not None else tok
            self.waiting_token_stack.append( _new_newline( tok ) )
            self.waiting_token_stack.append( _new_dedent( tok ) )
            self.indents_stack.pop()
        return self.nextToken()


    def HandleLeadingSpace( self, tok ):

        next_tok = self.base_source.nextToken()

        if next_tok.getType() == EeyoreLexer.EOF:
            # If we are at the end, emit some dedents and stop
            return self.DedentToLeft( next_tok )

        self.waiting_token_stack.append( next_tok )

        if next_tok.getType() == EeyoreLexer.NEWLINE:
            # If we find a line containing only a comment or nothing
            # but whitespace, just emit the newline (ignore the space)
            return self.nextToken()

        indent_col = len( tok.getText() )
        if ( indent_col % 4 ) != 0:
            raise EeyUserErrorException(
                "Indentation at the beginning of a line must be "
                + "4 spaces." )

        if indent_col > self.indents_stack[-1]:
            # Create an indent if we have moved to the right
            self.indents_stack.append( indent_col )
            self.waiting_token_stack.append( _new_indent( tok ) )
        else:
            # Create dedents until we hit a known value
            while indent_col < self.indents_stack[-1]:
                self.indents_stack.pop()
                #  We can't be dedenting unless we just had a newline
                assert( self.last_newline is not None )
                self.waiting_token_stack.append( _new_newline(
                    self.last_newline ) )
                self.waiting_token_stack.append( _new_dedent(
                    self.last_newline ) )

            if indent_col != self.indents_stack[-1]:
                raise EeyUserErrorException(
                    "Dedented to a level that does not match a previous "
                    + "indent level." )

        return self.nextToken() # TODO: emit an indent or dedent


