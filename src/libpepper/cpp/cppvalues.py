# Copyright (C) 2011-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

import sys

from cppbuiltins import *
from cpputils import render_statements
from special import *
from libpepper.builtins import *
from libpepper.functionvalues import *
from libpepper.languagevalues import *
from libpepper.values import *
from libpepper.builtinmodules.pepsys import PepSysArgv

def render_PepSymbol( value, env ):
    # In C++ (so far), we can just write the same symbol
    # we found in the Pepper.  For other output languages,
    # and possibly other Pepper structures, we will need
    # to break this up by "." and re-join it somehow, or
    # change the way we do this.
    return value.name()

def render_PepInt( value, env ):
    return str( value.value )

def render_PepFloat( value, env ):
    return str( value.value )

def render_PepBool( value, env ):
    if value.value:
        return "true"
    else:
        return "false"

def render_PepString( value, env ):
    return '"%s"' % value.value

def render_PepModification( value, env ):
    # TODO: assert they are addable and switch on how to add them
    return "%s += %s" % (
        value.var.render( env ), value.mod_value.render( env ) )

def render_PepPlus( value, env ):
    # TODO: assert they are addable and switch on how to add them
    return "(%s + %s)" % (
        value.left_value.render( env ), value.right_value.render( env ) )

def render_PepMinus( value, env ):
    # TODO: assert they are minusable and switch on how to minus them
    return "(%s - %s)" % (
        value.left_value.render( env ), value.right_value.render( env ) )

def render_PepTimes( value, env ):
    # TODO: assert they are timesable and switch on how to multiply them
    return "(%s * %s)" % (
        value.left_value.render( env ), value.right_value.render( env ) )

def render_PepGreaterThan( value, env ):
    # TODO: assert they are comparable
    return "(%s > %s)" % (
        value.left_value.render( env ), value.right_value.render( env ) )

def render_PepLessThan( value, env ):
    # TODO: assert they are comparable
    return "(%s < %s)" % (
        value.left_value.render( env ), value.right_value.render( env ) )


def render_PepIf( value, env ):
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

def render_PepFunction( value, env ):
    raise Exception( "Don't know how to render a function yet" )

def render_PepFunctionType( value, env ):
    # We only get here for return types - argument lists have special
    # handling because the name must be mixed with the type.
    # TODO: variable declarations should also not get here?
    return _render_function_pointer_type_and_name( value, "", env )

def render_PepFunctionOverloadList( value, env ):
    assert len( value._list ) > 0

    if len( value._list ) > 1:
        # TODO: How do we know which one you are referring to?
        raise Exception( "Can't (yet) use an overloaded function as a value." )

    # Pick the first one for now.
    fn = value._list[0]
    fakeargs = tuple(
        PepVariable( tn[0].evaluate( env ), tn[1].symbol_name )
            for tn in fn.arg_types_and_names
    )
    rtfn = PepRuntimeUserFunction( fn, fakeargs, None )
    name = env.renderer.add_function( rtfn, env )
    return name

def render_PepPrint( value, env ):
    return render_PepFunction( value, env )

def render_PepDef( value, env ):
    return ""

def render_PepPass( value, env ):
    return ""

def render_PepImport( value, env ):
    return ""

def render_PepInit( value, env ):
    if value.is_known( env ):
        return ""
    else:
        ev_var_type = value.var_type.evaluate( env )
        tp = value.var_type.render( env )
        name = value.var_name.symbol_name

        # TODO: avoid use of isinstance and __class__
        if isinstance( ev_var_type, PepUserClass ):
            # Remember the variable name in the renderer - we will use it
            # in render_PepRuntimeInit, which needs to know it even
            # though it shouldn't, because the init function is converted
            # from a normal one to one that passes the instance as its
            # first argument.
            env.renderer.init_variable_name = name
            rhs = value.init_value.render( env )
            env.renderer.init_variable_name = None
            return "%s %s; %s" % ( tp, name, rhs )

        elif ev_var_type.__class__ == PepFunctionType:
            rhs = value.init_value.render( env )
            lhs = _render_function_pointer_type_and_name(
                ev_var_type, value.var_name.symbol_name, env )
            return "%s = %s" % ( lhs, rhs )

        else:
            rhs = value.init_value.render( env )
            return "%s %s = %s" % ( tp, name, rhs )

type2string = {
    PepBool  : "bool",
    PepFloat : "double",
    PepInt   : "int", # Maybe should be intptr_t - I just can't bring myself
    PepVoid  : "void",
    }

def render_PepType( value, env ):
    if not value.is_known( env ):
        raise PepUserErrorException( v + " should be known!  "
            + "Pepper can't (currently) support types that are unknown at "
            + "compile time." )
        # TODO: ensure error message properly displays the unknown thing
    return type2string[value.value]

def render_PepNoneType( value, env ):
    return ""


def _render_normal_type( evald_type, env ):

    # TODO: deal with copyable types etc., which should have no ampersand
    # TODO: avoid isinstance?
    if (
        isinstance( evald_type, PepUserClass ) or
        isinstance( evald_type, PepConstructingUserClass )
    ):

        amp = "&"
    else:
        amp = ""

    return "%s%s" % (
        evald_type.render( env ),
        amp
    )

def _render_function_pointer_type_and_name( evald_type, name, env ):

    return "%s (*%s)( %s )" % (
        evald_type.return_type.render( env ),
        name,
        ", ".join(
            _render_normal_type( arg_type.evaluate( env ), env )
                for arg_type in evald_type.arg_types.items
        ),
    )


def _render_normal_type_and_name( evald_type, name, env ):

    # TODO: deal with copyable types etc., which should have no ampersand
    # TODO: avoid isinstance?
    if (
        isinstance( evald_type, PepUserClass ) or
        isinstance( evald_type, PepConstructingUserClass )
    ):

        amp = "&"
    else:
        amp = ""

    return "%s%s %s" % (
        evald_type.render( env ),
        amp,
        name
    )


def _render_type_and_name( typename, env ):
    evald_type = typename[0].evaluate( env )

    if isinstance( evald_type, PepFunctionType ):
        return _render_function_pointer_type_and_name(
            evald_type, typename[1].symbol_name, env )
    else:
        return _render_normal_type_and_name(
            evald_type, typename[1].symbol_name, env )

def _render_bracketed_list( items ):
    items_list = list( items )
    ret = "("
    if len( items_list ) > 0:
        ret += " "
        ret += ", ".join( items_list )
        ret += " "
    ret += ")"
    return ret

def render_PepUserClass_body( name, clazz, env ):
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


def render_PepuserFunction_signature( fn, args, name, env ):

    evald_ret_type = fn.ret_type.evaluate( env )

    types_and_names = izip(
        ( arg.evaluated_type( env ) for arg in args ),
        ( typename[1] for typename in fn.arg_types_and_names )
    )

    args_list = _render_bracketed_list(
        _render_type_and_name( typename, env ) for
            typename in types_and_names
    )

    # TODO: avoid __class__
    if evald_ret_type.__class__ == PepFunctionType:
        ret = _render_function_pointer_type_and_name(
            evald_ret_type, name + args_list, env )
    else:
        ret = fn.ret_type.render( env )
        ret += " "
        ret += name
        ret += args_list

    return ret

def render_PepUserFunction_forward_decl( name, func_call, env ):
    fn = func_call.user_function.evaluate( env )
    assert( fn.__class__ == PepUserFunction ) # TODO: handle other types

    ret = render_PepuserFunction_signature( fn, func_call.args, name, env )
    ret += ";\n"
    return ret

def render_PepUserFunction_body( name, func_call, env ):
    fn = func_call.user_function.evaluate( env )
    assert( fn.__class__ == PepUserFunction ) # TODO: handle other types

    ret = render_PepuserFunction_signature( fn, func_call.args, name, env )
    ret += "\n{\n"

    newenv = fn.execution_environment( func_call.args, False, env )

    for body_stmt in fn.body_stmts:
        st = body_stmt.ct_eval( newenv )
        if st.__class__ == PepPass:
            continue
        ret += indent_if_needed( st.render( newenv ) )

    ret += "}\n\n"

    return ret

def render_PepVar( value, env ):
    ret = ""

    for stmt in value.body_stmts:
        assert( stmt.__class__ == PepInit )
        ret += "    %s = %s;\n" % (
            stmt.var_name.symbol_name, stmt.init_value.render( env ) )

    return ret


def render_PepRuntimeUserFunction( value, env ):
    name = env.renderer.add_function( value, env )

    return ( name +
        _render_bracketed_list( arg.render( env ) for arg in value.args ) )

def render_PepRuntimeInit( value, env ):
    env.renderer.add_class( value.instance.clazz, env )
    name = env.renderer.add_def_init( value, env )

    # Use the variable name we remembered in render_PepInit
    return ( name +
        _render_bracketed_list(
            ( env.renderer.init_variable_name, ) + tuple(
                arg.render( env ) for arg in value.args )
        )
    )

def render_PepVariable( value, env ):
    # This is only called when rendering a function declaration (I think)
    # When a variable is actually used, the name of the symbol that is
    # used to refer to it is dumped directly in.
    return value.name

def render_PepFunctionCall( value, env ):
    fn = value.func.evaluate( env )
    if isinstance( fn, PepSymbol ): # TODO: can we do better than isinstance?
        # TODO: check arguments match?
        args = tuple( arg.render( env ) for arg in value.args )
        return render_PepSymbol( fn, env ) + _render_bracketed_list( args )
    else:
        # TODO: assert fn is callable
        return fn.call( value.args, env ).render( env )

def render_PepReturn( value, env ):
    return "return " + value.value.render( env )

def render_PepWhile( value, env ):
    return """while( {expression} )
    {{
        {body_statements}    }}""".format(
        expression = value.expression.render( env ),
        body_statements = render_statements( value.body_stmts, "", env ),
    )

def render_PepClass( value, env ):
    return ""

def render_PepInterface( value, env ):
    return ""

def render_PepUserClass( value, env ):
    return value.get_name()

def render_PepConstructingUserClass( value, env ):
    return value.get_name()

def render_PepArrayLookup( value, env ):
    # TODO: handle large numbers
    return value.array_value.render( env ) + "[%s]" % value.index.value

def render_PepSysArgv( value, env ):
    # TODO: set up a global variable called global_argv and initialise
    #       it at the beginning of main
    return "argv"

def type2renderer( tp ):
    return sys.modules[__name__].__dict__[ 'render_' + tp.__name__ ]

