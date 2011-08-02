
import EeyoreLexer
import EeyoreParser

def _render_text( token ):
    if token.getType() in (
            EeyoreLexer.LPAREN,
            EeyoreLexer.RPAREN,
            EeyoreLexer.NEWLINE,
            EeyoreLexer.LSQUBR,
            EeyoreLexer.RSQUBR,
            EeyoreLexer.INDENT,
            EeyoreLexer.DEDENT,
            ):
        return ""
    else:
        return "(%s)" % token.getText()

def _render_type( token ):
    return EeyoreParser._tokenNames[ token.getType() ]

def render_token( token ):
    return "%04d:%04d %10s%s" % (
        token.getLine(),
        token.getColumn(),
        _render_type( token ),
        _render_text( token ),
        )

