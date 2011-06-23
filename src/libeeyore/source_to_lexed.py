
from parse import EeyoreLexer
from parse import EeyoreParser

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

def source_to_lexed( source_in_fl, lexed_out_fl ):
    for token in EeyoreLexer.Lexer( source_in_fl ):
        lexed_out_fl.write( _render_token( token ) )
        lexed_out_fl.write( "\n" )

