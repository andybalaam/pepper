
import sys

from cppbuiltins import *
from libeeyore.builtins import *
from libeeyore.classvalues import *
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
        ev_var_type = value.var_type.evaluate( env )

        # TODO: avoid use of isinstance?
        if isinstance( ev_var_type, EeyUserClass ):
            # Remember the variable name in the renderer - we will use it
            # in render_EeyRuntimeInstance, which needs to know it even
            # though it shouldn't, because the init function is converted
            # from a normal one to one that passes the instance as its
            # first argument.
            env.renderer.init_variable_name = value.var_name.symbol_name
            subs = "%s %s; %s"
        else:
            subs = "%s %s = %s"

        return subs % (
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


def _render_type_and_name( env, typename ):
    evald_type = typename[0].evaluate( env )

    # TODO: deal with copyable types etc., which should have no ampersand
    # TODO: avoid isinstance?
    if isinstance( evald_type, EeyUserClass ):
        amp = "&"
    else:
        amp = ""

    return "%s%s %s" % (
        evald_type.render( env ),
        amp,
        typename[1].symbol_name
    )

def _render_bracketed_list( items ):
    items_list = list( items )
    ret = "("
    if len( items_list ) > 0:
        ret += " "
        ret += ", ".join( items_list )
        ret += " "
    ret += ")"
    return ret

def render_EeyUserClass_body( env, name, clazz ):
    ret = "struct %s\n{\n" % name

    for mem in clazz.member_variables:
        ret += "    %s %s;\n" % ( mem[0].render( env ), mem[1] )

    ret += "};\n\n"
    return ret

def render_statements( statements, env, indent ):
    ret = ""
    for stmt in statements:
        st = stmt.evaluate( env )
        if st.__class__ == EeyPass:
            continue
        ret += "%s%s;\n" % ( indent, st.render( env ) )
    return ret

def indent_if_needed( line ):
    if len( line ) == 0 or line[0] == " ":
        return line
    else:
        return "    %s;\n" % line

def render_EeyUserFunction_body( env, name, func_call ):
    fn = func_call.user_function.evaluate( env )

    assert( fn.__class__ == EeyUserFunction ) # TODO: handle other types

    ret = fn.ret_type.render( env )
    ret += " "
    ret += name
    ret += _render_bracketed_list( _render_type_and_name( env, typename ) for
        typename in fn.arg_types_and_names )
    ret += "\n{\n"

    newenv = fn.execution_environment( env, func_call.args, False )

    for body_stmt in fn.body_stmts:
        st = body_stmt.evaluate( newenv )
        if st.__class__ == EeyPass:
            continue
        ret += indent_if_needed( st.render( newenv ) )

    ret += "}\n\n"

    return ret

def render_EeyVar( env, value ):
    ret = ""

    for stmt in value.body_stmts:
        assert( stmt.__class__ == EeyInit )
        ret += "    %s = %s;\n" % (
            stmt.var_name.symbol_name, stmt.init_value.render( env ) )

    return ret


def render_EeyRuntimeUserFunction( env, value ):
    name = env.renderer.add_function( env, value )

    return ( name +
        _render_bracketed_list( arg.render( env ) for arg in value.args ) )

def render_EeyRuntimeInit( env, value ):
    env.renderer.add_class( env, value.instance.clazz )
    name = env.renderer.add_def_init( env, value )

    # Use the variable name we remembered in render_EeyInit
    return ( name +
        _render_bracketed_list(
            ( env.renderer.init_variable_name, ) + tuple(
                arg.render( env ) for arg in value.args )
        )
    )

def render_EeyRuntimeInstance( env, value ):
    return value.name

def render_EeyFunctionCall( env, value ):
    fn = value.func.evaluate( env )

    # TODO: assert fn is callable

    return fn.call( env, value.args ).render( env )

def render_EeyReturn( env, value ):
    return "return " + value.value.render( env )


def render_EeyClass( env, value ):
    return ""

def render_EeyUserClass( env, value ):
    return value.name

def render_EeyInstance( env, value ):
    return ""

def render_EeyArrayLookup( env, value ):
    # TODO: handle large numbers
    return value.array_value.render( env ) + "[%s]" % value.index.value

def render_EeySysArgv( env, value ):
    # TODO: set up a global variable called global_argv and initialise
    #       it at the beginning of main
    return "argv"

def type2renderer( tp ):
    return sys.modules[__name__].__dict__[ 'render_' + tp.__name__ ]

