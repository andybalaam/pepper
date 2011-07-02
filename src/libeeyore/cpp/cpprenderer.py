
import cppvalues

class EeyCppRenderer( object ):
    def __init__( self ):
        self.headers = []
        self.functions = []

    def value_renderer( self, value ):
        return cppvalues.type2renderer[ value.__class__ ]

    def render_exe( self, values, env ):
        rendered_lines = [value.render( env ) for value in values]
        ret = "\n".join( "#include <%s>" % h for h in self.headers )
        ret += "\n\nint main( int argc, char* argv[] )\n{\n"

        for ln in filter( lambda x: len( x ) != 0, rendered_lines ):
            ret += "    "
            ret += ln
            ret += ";\n"

        ret += "\n    return 0;\n"
        ret += "}\n"

        return ret
