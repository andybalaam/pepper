
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

def _function_signature_string( env, user_function ):
    ret = user_function.name
    ret += "_eey_s_eey_"
    ret += "_eey_s_eey_".join(
        str( tn[0].evaluate( env ).value.__name__ ) for
            tn in user_function.arg_types_and_names )
    return ret

def _overload_name( name, num_overloads ):
    return "%s_eey_%d" % ( name, num_overloads )

class EeyCppRenderer( object ):
    def __init__( self ):
        self._headers = []
        self._functions = {} # name -> signature -> ( name, rendered body )

    def add_header( self, header ):
        if header not in self._headers:
            self._headers.append( header )

    def add_function( self, env, runtime_function ):
        signature = _function_signature_string(
            env, runtime_function.user_function )

        name = runtime_function.user_function.name
        if name not in self._functions:
            self._functions[name] = {}

        overloads = self._functions[name]

        # If we have't rendered this function already, do it now
        if signature in overloads:
            name = overloads[signature][0]
        else:

            num_overloads = len( overloads )
            if num_overloads > 0:
                name = _overload_name( name, num_overloads )

            rendered = cppvalues.render_EeyUserFunction_body(
                env, name, runtime_function )

            overloads[signature] = ( name, rendered )

        return name

    def value_renderer( self, value ):
        return cppvalues.type2renderer( value.__class__ )

    def render_exe( self, values, env ):
        rendered_lines = [ _render_with_semicolon( value, env )
            for value in values ]
        ret = ""
        for h in self._headers:
            ret += "#include <%s>\n" % h
        ret += "\n"
        for overloads in self._functions.values():
            for name, rendered_fn in sorted( overloads.values() ):
                ret += rendered_fn
        ret += "int main( int argc, char* argv[] )\n{\n"

        for ln in filter( lambda x: len( x ) != 0, rendered_lines ):
            ret += "    "
            ret += ln
            ret += "\n"

        ret += "\n    return 0;\n"
        ret += "}\n"

        return ret
