# Copyright (C) 2011-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


import PepperLexer
import PepperParser

def _render_text( token ):
    if token.getType() in (
            PepperLexer.LPAREN,
            PepperLexer.RPAREN,
            PepperLexer.NEWLINE,
            PepperLexer.LSQUBR,
            PepperLexer.RSQUBR,
            PepperLexer.INDENT,
            PepperLexer.DEDENT,
            ):
        return ""
    else:
        return "(%s)" % token.getText()

def _render_type( token ):
    return PepperParser._tokenNames[ token.getType() ]

def render_token( token ):
    return "%04d:%04d %10s%s" % (
        token.getLine(),
        token.getColumn(),
        _render_type( token ),
        _render_text( token ),
        )

