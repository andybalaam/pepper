
from libeeyore.languagevalues import EeyIf

import cppvalues

def _has_semicolon( val ):
    cls = val.__class__
    if cls == EeyIf:
        return False
    else:
        return True

def _render_with_semicolon( value, env ):
    val = value.evaluate( env )
    ret = val.render( env )
    if ret != "" and _has_semicolon( val ):
        ret += ";"
    return ret

class EeyCppRenderer( object ):
    def __init__( self ):
        self._headers = []
        self._functions = {}

    def add_header( self, header ):
        if header not in self._headers:
            self._headers.append( header )

    def add_function( self, env, function ):
        rend_body = cppvalues.render_EeyUserFunction_body( env, function )
        self._functions[ function.user_function.name ] = rend_body

    def value_renderer( self, value ):
        return cppvalues.type2renderer( value.__class__ )

    def render_exe( self, values, env ):
        rendered_lines = [ _render_with_semicolon( value, env )
            for value in values ]
        ret = ""
        for h in self._headers:
            ret += "#include <%s>\n" % h
        ret += "\n"
        if len( self._functions ) > 0:
            for fn in self._functions.values():
                ret += fn
            ret += "\n"
        ret += "int main( int argc, char* argv[] )\n{\n"

        for ln in filter( lambda x: len( x ) != 0, rendered_lines ):
            ret += "    "
            ret += ln
            ret += "\n"

        ret += "\n    return 0;\n"
        ret += "}\n"

        return ret
