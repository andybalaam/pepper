# Copyright (C) 2011-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


import sys

from cppbuiltins import *
from cpputils import render_statements
from special import *
from libpepper.builtins import *
from libpepper.classvalues import *
from libpepper.functionvalues import *
from libpepper.languagevalues import *
from libpepper.values import *
from libpepper.builtinmodules.eeysys import EeySysArgv

def render_EeySymbol( value, env ):
    return value.name()

def render_EeyInt( value, env ):
    return str( value.value )

def render_EeyFloat( value, env ):
    return str( value.value )

def render_EeyBool( value, env ):
    if value.value:
        return "true"
    else:
        return "false"

def render_EeyString( value, env ):
    return '"%s"' % value.value

def render_EeyModification( value, env ):
    # TODO: assert they are addable and switch on how to add them
    return "%s += %s" % (
        value.var.render( env ), value.mod_value.render( env ) )

def render_EeyPlus( value, env ):
    # TODO: assert they are addable and switch on how to add them
    return "(%s + %s)" % (
        value.left_value.render( env ), value.right_value.render( env ) )

def render_EeyMinus( value, env ):
    # TODO: assert they are minusable and switch on how to minus them
    return "(%s - %s)" % (
        value.left_value.render( env ), value.right_value.render( env ) )

def render_EeyTimes( value, env ):
    # TODO: assert they are timesable and switch on how to multiply them
    return "(%s * %s)" % (
        value.left_value.render( env ), value.right_value.render( env ) )

def render_EeyGreaterThan( value, env ):
    # TODO: assert they are comparable
    return "(%s > %s)" % (
        value.left_value.render( env ), value.right_value.render( env ) )


def render_EeyIf( value, env ):
    # TODO: assert predicate is a bool or function returning one

    else_block = ""
    if value.cmds_if_false is not None:
        else_block = """
    else
    {{
        {cmds_if_false}    }}""".format(
            cmds_if_false = render_statements(
                value.cmds_if_false, "", env )
            )

    return """if( {predicate} )
    {{
        {cmds_if_true}    }}{else_block}""".format(
        predicate = value.predicate.render( env ),
        cmds_if_true = render_statements( value.cmds_if_true, "", env ),
        else_block = else_block
        )

def render_EeyFunction( value, env ):
    raise Exception( "Don't know how to render a function yet" )

def render_EeyPrint( value, env ):
    return render_EeyFunction( value, env )

def render_EeyDef( value, env ):
    return ""

def render_EeyPass( value, env ):
    return ""

def render_EeyImport( value, env ):
    return ""

def render_EeyInit( value, env ):
    if value.is_known( env ):
        return ""
    else:
        ev_var_type = value.var_type.evaluate( env )

        # TODO: avoid use of isinstance?
        if isinstance( ev_var_type, EeyUserClass ):
            # Remember the variable name in the renderer - we will use it
            # in render_EeyRuntimeInit, which needs to know it even
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

def render_EeyType( value, env ):
    if not value.is_known( env ):
        raise EeyUserErrorException( v + " should be known!  "
            + "Pepper can't (currently) support types that are unknown at "
            + "compile time." )
        # TODO: ensure error message properly displays the unknown thing
    return type2string[value.value]

def render_EeyNoneType( value, env ):
    return ""


def _render_type_and_name( typename, env ):
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

def render_EeyUserClass_body( name, clazz, env ):
    ret = "struct %s\n{\n" % name

    for mem in clazz.member_variables:
        ret += "    %s %s;\n" % ( mem[0].render( env ), mem[1] )

    ret += "};\n\n"
    return ret

def indent_if_needed( line ):
    if len( line ) == 0 or line[0] == " ":
        return line
    else:
        return "    %s;\n" % line

def render_EeyUserFunction_body( name, func_call, env ):
    fn = func_call.user_function.evaluate( env )

    assert( fn.__class__ == EeyUserFunction ) # TODO: handle other types

    ret = fn.ret_type.render( env )
    ret += " "
    ret += name
    ret += _render_bracketed_list( _render_type_and_name( typename, env ) for
        typename in fn.arg_types_and_names )
    ret += "\n{\n"

    newenv = fn.execution_environment( func_call.args, False, env )

    for body_stmt in fn.body_stmts:
        st = body_stmt.evaluate( newenv )
        if st.__class__ == EeyPass:
            continue
        ret += indent_if_needed( st.render( newenv ) )

    ret += "}\n\n"

    return ret

def render_EeyVar( value, env ):
    ret = ""

    for stmt in value.body_stmts:
        assert( stmt.__class__ == EeyInit )
        ret += "    %s = %s;\n" % (
            stmt.var_name.symbol_name, stmt.init_value.render( env ) )

    return ret


def render_EeyRuntimeUserFunction( value, env ):
    name = env.renderer.add_function( value, env )

    return ( name +
        _render_bracketed_list( arg.render( env ) for arg in value.args ) )

def render_EeyRuntimeInit( value, env ):
    env.renderer.add_class( value.instance.clazz, env )
    name = env.renderer.add_def_init( value, env )

    # Use the variable name we remembered in render_EeyInit
    return ( name +
        _render_bracketed_list(
            ( env.renderer.init_variable_name, ) + tuple(
                arg.render( env ) for arg in value.args )
        )
    )

def render_EeyRuntimeInstance( value, env ):
    return value.var_name

def render_EeyFunctionCall( value, env ):
    fn = value.func.evaluate( env )

    # TODO: assert fn is callable

    return fn.call( value.args, env ).render( env )

def render_EeyReturn( value, env ):
    return "return " + value.value.render( env )


def render_EeyClass( value, env ):
    return ""

def render_EeyUserClass( value, env ):
    return value.name

def render_EeyArrayLookup( value, env ):
    # TODO: handle large numbers
    return value.array_value.render( env ) + "[%s]" % value.index.value

def render_EeySysArgv( value, env ):
    # TODO: set up a global variable called global_argv and initialise
    #       it at the beginning of main
    return "argv"

def type2renderer( tp ):
    return sys.modules[__name__].__dict__[ 'render_' + tp.__name__ ]

