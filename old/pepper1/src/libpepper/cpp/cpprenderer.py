# Copyright (C) 2011-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


from libpepper.vals.all_values import *
from libpepper.utils.type_is import type_is

import cppvalues

def _has_semicolon( val ):
    cls = val.__class__
    if cls in ( PepIf, PepFor ):
        return False
    else:
        return True

def _render_with_semicolon( value, env ):
    val = value.ct_eval( env )
    ret = val.render( env )
    if ret != "" and _has_semicolon( val ):
        ret += ";"
    return ret

def _function_signature_string( runtime_function, env ):
    ret = runtime_function.user_function.name
    ret += "_pep_s_pep_"
    ret += "_pep_s_pep_".join(
        str( a.evaluated_type( env ).get_name() )
            for a in runtime_function.args )
    return ret

def _overload_name( name, num_overloads ):
    return "%s_pep_%d" % ( name, num_overloads )

class PepCppRenderer( object ):
    def __init__( self ):
        self._headers = []
        self._functions = {} # name -> signature -> ( name, rendered body )
        self._classes = {} # name -> rendered_body
        self.init_variable_name = None

    def add_header( self, header ):
        if header not in self._headers:
            self._headers.append( header )

    def add_function( self, runtime_function, env ):
        signature = _function_signature_string(
            runtime_function, env )

        if runtime_function.namespace_name is not None:
            name = runtime_function.namespace_name
            name += "_pep_c_pep_"
        else:
            name = ""

        name += runtime_function.user_function.name
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

            rendered = cppvalues.render_PepUserFunction_body(
                name, runtime_function, env )

            forward_decl = cppvalues.render_PepUserFunction_forward_decl(
                name, runtime_function, env )

            overloads[signature] = ( name, rendered, forward_decl )

        return name

    def add_def_init( self, runtime_init, env ):
        type_is( PepRuntimeInit, runtime_init )
        type_is( PepEnvironment, env )

        fn = runtime_init.init_fn.user_function

        clazz = runtime_init.instance.clazz

        clazz_type_and_name = (
            PepConstructingUserClass( clazz ), PepSymbol("self") )

        init_style_arg_types_and_names = (
            (clazz_type_and_name,) + fn.arg_types_and_names[1:] )

        init_style_fn = PepRuntimeUserFunction(
            PepUserFunction(
                fn.name,
                fn.ret_type,
                init_style_arg_types_and_names,
                fn.body_stmts
            ),
            runtime_init.init_fn.args,
            runtime_init.instance.clazz.name
        )

        return self.add_function( init_style_fn, env )


    def add_class( self, clazz, env ):
        # TODO: handle clashes - if same, no problem, if different, fail?
        name = clazz.name
        self._classes[ name ] = cppvalues.render_PepUserClass_body(
            name, clazz, env )



    def value_renderer( self, value ):
        return cppvalues.type2renderer( value.__class__ )

    def render_exe( self, values, env ):
        rendered_lines = [ _render_with_semicolon( value, env )
            for value in values ]
        ret = ""
        for h in self._headers:
            ret += "#include <%s>\n" % h
        ret += "\n"

        for rendered_clazz in self._classes.values():
            ret += rendered_clazz

        for overloads in self._functions.values():
            for name, rendered_fn, forward_decl in sorted( overloads.values() ):
                ret += forward_decl
        if len( self._functions ) > 0:
            ret += "\n"

        for overloads in self._functions.values():
            for name, rendered_fn, forward_decl in sorted( overloads.values() ):
                ret += rendered_fn

        ret += "int main( int argc, char* argv[] )\n{\n"

        for ln in filter( lambda x: len( x ) != 0, rendered_lines ):
            ret += "    "
            ret += ln
            ret += "\n"

        ret += "\n    return 0;\n"
        ret += "}\n"

        return ret
