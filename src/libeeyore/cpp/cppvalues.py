
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


def render_EeyGreaterThan( env, value ):
    # TODO: assert they are comparable
    return "(%s > %s)" % (
        value.left_value.render( env ), value.right_value.render( env ) )


def render_EeyIf( env, value ):
    # TODO: assert predicate is a bool or function returning one
    return "if( %s )\n    {\n        %s;\n    }" % (
        value.predicate.render( env ),
        "\n        ".join( c.render(env) for c in value.cmds_if_true )
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
    EeyBool : "bool",
    EeyInt  : "int",
    EeyVoid : "void",
    }

def render_EeyType( env, value ):
    return type2string[value.value]

def render_EeyNoneType( env, value ):
    return ""


def render_type_and_name( env, typename ):
    return "%s %s" % ( render_EeyType( env, typename[0] ),
        typename[1].symbol_name )

def render_EeyUserFunction_body( env, func_call ):
    fn = func_call.user_function.evaluate( env )

    assert( fn.__class__ == EeyUserFunction ) # TODO: handle other types

    ret = fn.ret_type.render( env )
    ret += " "
    ret += fn.name
    ret += "( "
    ret += ", ".join( render_type_and_name( env, typename ) for typename
        in fn.arg_types_and_names )
    ret += " )\n{\n"

    newenv = fn.execution_environment( env, func_call.args, False )

    # TODO: not every statement should be a return
    for body_stmt in fn.body_stmts:
        ret += "    return %s;\n" % body_stmt.render( newenv )

    ret += "}\n"

    return ret

def render_EeyRuntimeUserFunction( env, value ):
    env.renderer.functions.append( render_EeyUserFunction_body(
        env, value ) )

    return ( value.user_function.name + "( " +
        ", ".join( arg.render( env ) for arg in value.args )
        + " )" )

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

type2renderer = {
    EeyArrayLookup          : render_EeyArrayLookup,
    EeyBool                 : render_EeyBool,
    EeyDef                  : render_EeyDef,
    EeyFunction             : render_EeyFunction,
    EeyFunctionCall         : render_EeyFunctionCall,
    EeyGreaterThan          : render_EeyGreaterThan,
    EeyIf                   : render_EeyIf,
    EeyImport               : render_EeyImport,
    EeyInit                 : render_EeyInit,
    EeyInt                  : render_EeyInt,
    EeyNoneType             : render_EeyNoneType,
    EeyPass                 : render_EeyPass,
    EeyPlus                 : render_EeyPlus,
    EeyPrint                : render_EeyPrint,
    EeyReturn               : render_EeyReturn,
    EeyRuntimeLen           : render_EeyRuntimeLen,
    EeyRuntimePrint         : render_EeyRuntimePrint,
    EeyRuntimeUserFunction  : render_EeyRuntimeUserFunction,
    EeyString               : render_EeyString,
    EeySymbol               : render_EeySymbol,
    EeySysArgv              : render_EeySysArgv,
    EeyType                 : render_EeyType,
    }


