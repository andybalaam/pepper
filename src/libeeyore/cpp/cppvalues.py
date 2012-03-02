
import sys

from cppbuiltins import *
from libeeyore.builtins import *
from libeeyore.functionvalues import *
from libeeyore.languagevalues import *
from libeeyore.values import *
from libeeyore.builtinmodules.eeysys import EeySysArgv

def render_EeySymbol( env, value ):
    return value.name()

def render_EeyInt( env, value ):
    return str( value.value )

def render_EeyFloat( env, value ):
    return str( value.value )

def render_EeyBool( env, value ):
    if value.value:
        return "true"
    else:
        return "false"

def render_EeyString( env, value ):
    return '"%s"' % value.value

def render_EeyPlus( env, value ):
    # TODO: assert they are addable and switch on how to add them
    return "(%s + %s)" % (
        value.left_value.render( env ), value.right_value.render( env ) )

def render_EeyTimes( env, value ):
    # TODO: assert they are timesable and switch on how to multiply them
    return "(%s * %s)" % (
        value.left_value.render( env ), value.right_value.render( env ) )

def render_EeyGreaterThan( env, value ):
    # TODO: assert they are comparable
    return "(%s > %s)" % (
        value.left_value.render( env ), value.right_value.render( env ) )


def _render_cmds( cmds, env ):
    return "\n        ".join( c.render(env) for c in cmds )

def render_EeyIf( env, value ):
    # TODO: assert predicate is a bool or function returning one

    else_block = ""
    if value.cmds_if_false is not None:
        else_block = """
    else
    {{
        {cmds_if_false};
    }}""".format(
            cmds_if_false = _render_cmds( value.cmds_if_false, env )
            )

    return """if( {predicate} )
    {{
        {cmds_if_true};
    }}{else_block}""".format(
        predicate = value.predicate.render( env ),
        cmds_if_true = _render_cmds( value.cmds_if_true,  env ),
        else_block = else_block
        )

def render_EeyFunction( env, value ):
    raise Exception( "Don't know how to render a function yet" )

def render_EeyPrint( env, value ):
    return render_EeyFunction( env, value )

def render_EeyDef( env, value ):
    return ""

def render_EeyPass( env, value ):
    return ""

def render_EeyImport( env, value ):
    return ""

def render_EeyInit( env, value ):
    if value.is_known( env ):
        return ""
    else:
        return "%s %s = %s" % (
                value.var_type.render( env ),
                value.var_name.symbol_name,
                value.init_value.render( env ),
            )

type2string = {
    EeyBool  : "bool",
    EeyFloat : "double",
    EeyInt   : "int", # Maybe should be intptr_t - I just can't bring myself
    EeyVoid  : "void",
    }

def render_EeyType( env, value ):
    if not value.is_known( env ):
        raise EeyUserErrorException( v + " should be known!  "
            + "Eeyore can't (currently) support types that are unknown at "
            + "compile time." )
        # TODO: ensure error message properly displays the unknown thing
    return type2string[value.value]

def render_EeyNoneType( env, value ):
    return ""


def render_type_and_name( env, typename ):
    return "%s %s" % ( render_EeyType( env, typename[0].evaluate( env ) ),
        typename[1].symbol_name )

def _render_bracketed_list( items ):
    items_list = list( items )
    ret = "("
    if len( items_list ) > 0:
        ret += " "
        ret += ", ".join( items_list )
        ret += " "
    ret += ")"
    return ret

def render_EeyUserFunction_body( env, func_call ):
    fn = func_call.user_function.evaluate( env )

    assert( fn.__class__ == EeyUserFunction ) # TODO: handle other types

    ret = fn.ret_type.render( env )
    ret += " "
    ret += fn.name
    ret += _render_bracketed_list( render_type_and_name( env, typename ) for
        typename in fn.arg_types_and_names )
    ret += "\n{\n"

    newenv = fn.execution_environment( env, func_call.args, False )

    for body_stmt in fn.body_stmts:
        st = body_stmt.evaluate( newenv )
        if st.__class__ == EeyPass:
            continue
        ret += "    %s;\n" % st.render( newenv )

    ret += "}\n"

    return ret

def render_EeyRuntimeUserFunction( env, value ):
    env.renderer.add_function( env, value )

    return ( value.user_function.name +
        _render_bracketed_list( arg.render( env ) for arg in value.args ) )

def render_EeyFunctionCall( env, value ):

    fn = value.func.evaluate( env )

    # TODO: assert fn is callable

    return fn.call( env, value.args ).render( env )

def render_EeyReturn( env, value ):
    return "return " + value.value.render( env )


def render_EeyArrayLookup( env, value ):
    # TODO: handle large numbers
    return value.array_value.render( env ) + "[%s]" % value.index.value

def render_EeySysArgv( env, value ):
    # TODO: set up a global variable called global_argv and initialise
    #       it at the beginning of main
    return "argv"

def type2renderer( tp ):
    return sys.modules[__name__].__dict__[ 'render_' + tp.__name__ ]

