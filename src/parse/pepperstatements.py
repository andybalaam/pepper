# Copyright (C) 2011-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


import PepperParser
import PepperTreeWalker

class PepperStatements( object ):
    def __init__( self, token_stream ):
         parser = PepperParser.Parser( token_stream )
         parser.program();
         self._walker = PepperTreeWalker.Walker()
         self._ast = parser.getAST()

    def at_end( self ):
        return self._ast.getType() == PepperParser.EOF_TYPE

    def __iter__( self ):
        return self

    def next( self ):
        if self.at_end():
            raise StopIteration()
        ret = None
        while ret is None:
            ret = self._walker.statement( self._ast )
            self._ast = self._ast.getNextSibling()
            if self.at_end() and ret is None:
                raise StopIteration()
        return ret

