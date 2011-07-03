
from antlr import CommonToken
from antlr import Token
from antlr import TokenStream

class Iterable2TokenStream( TokenStream ):
    def __init__( self, lst ):
        self.it = iter( lst )

    def nextToken( self ):
        try:
            return self.it.next()
        except StopIteration:
            return CommonToken( type = Token.EOF_TYPE )


def make_token( text, tp, line = None, column = None ):
    ret = CommonToken()
    ret.setText( text )
    ret.setType( tp )
    if line is not None:
        ret.setLine( line )
    if column is not None:
        ret.setLine( column )
    return ret


