# Copyright (C) 2011-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


class IterableFromTokenStream( object ):
    """
    A mix-in class you can inherit from if you are a token stream
    and want people to be able to iterate through your tokens
    """

    def __iter__( self ):
        return self

    def next( self ):
        nxt = self.nextToken()
        if nxt.getType() == antlr.Token.EOF_TYPE:
            raise StopIteration()
        return nxt

