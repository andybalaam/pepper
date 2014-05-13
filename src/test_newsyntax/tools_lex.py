from tools import *
from cStringIO import StringIO
from nose.tools import *

import re

from newsyntaxparse import NewSyntaxPepperLexer

whitespace_re = re.compile( r'\s+' )
def _simplify_lexed( lexed ):
    return whitespace_re.sub( " ", lexed )

def _lex( string ):
    return list( NewSyntaxPepperLexer.Lexer( StringIO( string ) ) )

def _format_token( token ):
    tp = token.getType()
    if tp == NewSyntaxPepperLexer.SYMBOL:
        return "symbol:" + token.getText()
    elif tp == NewSyntaxPepperLexer.INT:
        return "int:" + token.getText()
    else:
        return token.getText()

def _format_lexed( lexed ):
    return " ".join( ( _format_token( tok ) for tok in lexed ) )

def assert_lex( code, result ):
    assert_equals( result, _format_lexed( _lex( code ) ) )

