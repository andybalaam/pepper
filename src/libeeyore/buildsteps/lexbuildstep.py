
from buildstep import BuildStep
from parse import EeyoreLexer
from parse import EeyoreParser
from parse.eeyoretokenstreamfromfile import EeyoreTokenStreamFromFile


def _render_text( token ):
    if token.getType() in ( EeyoreLexer.LPAREN, EeyoreLexer.RPAREN ):
        return ""
    else:
        return "(%s)" % token.getText()

def _render_type( token ):
    return EeyoreParser._tokenNames[ token.getType() ]

def _render_token( token ):
    return "%04d:%04d %10s%s" % (
        token.getLine(),
        token.getColumn(),
        _render_type( token ),
        _render_text( token ),
        )


class LexBuildStep( BuildStep ):
    def read_from_file( self, fl ):
        return EeyoreTokenStreamFromFile( fl )

    def process( self, val ):
        return EeyoreLexer.Lexer( val )

    def write_to_file( self, val, fl ):
        for token in val:
            fl.write( _render_token( token ) )
            fl.write( "\n" )

