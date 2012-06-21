
from nose.tools import *

from libeeyore import builtins
from libeeyore.environment import EeyEnvironment
from libeeyore.namespace import EeyNamespace
from libeeyore.cpp.cppvalues import *
from libeeyore.cpp.cpprenderer import EeyCppRenderer

def test_Const_int_value_renders_as_a_number():
    env = EeyEnvironment( EeyCppRenderer() )
    value = EeyInt( "23" )

    assert_equal( value.render( env ), "23" )

def test_Const_float_value_renders_as_a_number():
    env = EeyEnvironment( EeyCppRenderer() )
    value = EeyFloat( "23.65" )

    assert_equal( value.render( env ), "23.65" )



def test_Const_string_value_renders_as_a_string():
    env = EeyEnvironment( EeyCppRenderer() )
    value = EeyString( "foo" )

    assert_equal( value.render( env ), '"foo"' )


def test_Variable_referring_to_known_int_renders_like_an_int():
    env = EeyEnvironment( EeyCppRenderer() )
    env.namespace["myvariable"] = EeyInt( "23" )

    value = EeySymbol( "myvariable" )

    assert_equal( value.render( env ), "23" )


def test_Variable_in_subnamespace_is_found():

    # Something with a "namespace" member.  In real life, this would
    # be an EeyUserClass or similar.
    class NsHolder( EeyValue ):
        def __init__( self ):
            EeyValue.__init__( self )
            self.namespace = EeyNamespace()
        def construction_args( self ):
            return ()
        def get_namespace( self ):
            return self.namespace

    nsholder = NsHolder()

    basens = EeyNamespace()
    basens["MyHolder"] = nsholder

    env = EeyEnvironment( EeyCppRenderer(), basens )

    nsholder.namespace["myheld"] = EeyInt( "355" )

    value = EeySymbol( "MyHolder.myheld" )

    assert_equal( value.render( env ), "355" )



def test_Subnamespace_referred_by_symbol_is_found():

    # Something with a "namespace" member.  In real life, this would
    # be an EeyUserClass or similar.
    class NsHolder( EeyValue ):
        def __init__( self ):
            EeyValue.__init__( self )
            self.namespace = EeyNamespace()
        def get_namespace( self ):
            return self.namespace

        def construction_args( self ):
            return ()

    nsholder = NsHolder()

    basens = EeyNamespace()
    basens["MyHolder"] = nsholder
    basens["RefHolder"] = EeySymbol( "MyHolder" )

    env = EeyEnvironment( EeyCppRenderer(), basens )

    nsholder.namespace["myheld"] = EeyInt( "356" )

    value = EeySymbol( "RefHolder.myheld" )

    assert_equal( value.render( env ), "356" )



def test_Add_two_known_ints_renders_calculated_sum():
    env = EeyEnvironment( EeyCppRenderer() )
    value = EeyPlus( EeyInt( "2" ), EeyInt( "3" ) )

    assert_equal( value.render( env ), "5" )

def test_Add_two_known_floats_renders_calculated_sum():
    env = EeyEnvironment( EeyCppRenderer() )
    value = EeyPlus( EeyFloat( "2.9" ), EeyFloat( "3.1" ) )

    assert_equal( value.render( env ), "6.0" )


def test_Unknown_variable_renders_as_symbol():
    env = EeyEnvironment( EeyCppRenderer() )
    env.namespace["myvariable"] = EeyVariable( EeyType( EeyInt ) )

    value = EeySymbol( "myvariable" )

    assert_equal( value.render( env ), "myvariable" )

def test_Add_Unknown_to_known_literal_renders_uncalculated_sum():
    env = EeyEnvironment( EeyCppRenderer() )
    env.namespace["input"] = EeyVariable( EeyType( EeyInt ) )

    value = EeyPlus( EeyInt( "4" ), EeySymbol( "input" ) )

    assert_equal( value.render( env ), "(4 + input)" )

def test_Add_Unknown_to_known_symbol_renders_uncalculated_sum():
    env = EeyEnvironment( EeyCppRenderer() )
    env.namespace["input"] = EeyVariable( EeyType( EeyInt ) )
    env.namespace["four"] = EeyInt( "4" )

    value = EeyPlus( EeySymbol( "input" ), EeySymbol( "four" ) )

    assert_equal( value.render( env ), "(input + 4)" )


def test_Unknown_inside_nested_plus_causes_whole_sum_to_be_uncalculated():
    env = EeyEnvironment( EeyCppRenderer() )
    env.namespace["input"] = EeyVariable( EeyType( EeyInt ) )

    value = EeyPlus( EeyInt( "4" ),
        EeyPlus( EeyInt( "5" ), EeySymbol( "input" ) ) )

    assert_equal( value.render( env ), "(4 + (5 + input))" )


def test_Print_string_renders_as_printf():
    env = EeyEnvironment( EeyCppRenderer() )
    builtins.add_builtins( env )

    value = EeyFunctionCall( EeySymbol( "print" ),
        ( EeyString( "hello" ), ) )

    assert_equal( value.render( env ), 'printf( "hello\\n" )' )
    assert_equal( env.renderer._headers, [ "stdio.h" ] )


def test_Print_unknown_int_renders_as_percent_d():
    env = EeyEnvironment( EeyCppRenderer() )
    builtins.add_builtins( env )

    init = EeyInit(
        EeyType( EeyInt ), EeySymbol( "i" ), EeyVariable( EeyType( EeyInt ) ) )

    init.evaluate( env )

    value = EeyFunctionCall( EeySymbol( "print" ),
        ( EeySymbol( "i" ), ) )

    assert_equal( value.render( env ), 'printf( "%d\\n", i )' )


def test_Print_unknown_float_renders_as_percent_f():
    env = EeyEnvironment( EeyCppRenderer() )
    builtins.add_builtins( env )

    init = EeyInit(
        EeyType( EeyFloat ), EeySymbol( "f" ),
        EeyVariable( EeyType( EeyFloat ) )
    )

    init.evaluate( env )

    value = EeyFunctionCall( EeySymbol( "print" ),
        ( EeySymbol( "f" ), ) )

    assert_equal( value.render( env ), 'printf( "%f\\n", f )' )



def test_Print_unknown_bool_renders_as_percent_s_colon_op():
    env = EeyEnvironment( EeyCppRenderer() )
    builtins.add_builtins( env )

    init = EeyInit(
        EeyType( EeyBool ), EeySymbol( "b" ),
        EeyVariable( EeyType( EeyBool ) )
    )

    init.evaluate( env )

    value = EeyFunctionCall( EeySymbol( "print" ),
        ( EeySymbol( "b" ), ) )

    assert_equal(
        value.render( env ),
        'printf( "%s\\n", (b ? "true" : "false") )' )




def test_known_array_lookup():
    env = EeyEnvironment( EeyCppRenderer() )

    # int[] myarr = [3,4,5]
    # myarr[1]

    env.namespace["myarr"] = EeyArray( EeyType( EeyInt ), (
        EeyInt( "3" ), EeyInt( "4" ), EeyInt( "5" ), ) )

    value = EeyArrayLookup( EeySymbol( "myarr" ), EeyInt( "1" ) )

    assert_equal( value.render( env ), "4" )

def test_bool_true():
    env = EeyEnvironment( EeyCppRenderer() )
    value = EeyBool( True )
    assert_equal( value.render( env ), "true" )

def test_bool_false():
    env = EeyEnvironment( EeyCppRenderer() )
    value = EeyBool( False )
    assert_equal( value.render( env ), "false" )

@raises( EeyInitialisingWithWrongType )
def test_initialisation_wrong_type():
    env = EeyEnvironment( None )
    add_builtins( env )
    init = EeyInit( EeySymbol( "int" ), EeySymbol( "i" ), EeyString( "foo" ) )
    init.evaluate( env )


def test_known_initialisation_renders_nothing():
    env = EeyEnvironment( EeyCppRenderer() )
    add_builtins( env )
    init = EeyInit( EeySymbol( "int" ), EeySymbol( "i" ), EeyInt( "4" ) )
    assert_equal( init.render( env ), "" )

def test_unknown_initialisation_evaluates_to_self():
    env = EeyEnvironment( EeyCppRenderer() )
    add_builtins( env )
    env.namespace["unknown"] = EeyVariable( EeyType( EeyInt ) )
    init = EeyInit( EeySymbol( "int" ), EeySymbol( "i" ),
        EeySymbol( "unknown" ) )
    assert_equal( init.evaluate( env ), init )

def test_unknown_initialisation_renders():
    env = EeyEnvironment( EeyCppRenderer() )
    add_builtins( env )
    env.namespace["unknown"] = EeyVariable( EeyType( EeyInt ) )
    init = EeyInit( EeySymbol( "int" ), EeySymbol( "i" ),
        EeySymbol( "unknown" ) )
    assert_equal( init.render( env ), "int i = unknown" )


def test_unknown_initialisation_makes_symbol_valid():
    env = EeyEnvironment( EeyCppRenderer() )
    add_builtins( env )

    env.namespace["unknown"] = EeyVariable( EeyType( EeyInt ) )

    init = EeyInit( EeySymbol( "int" ), EeySymbol( "i" ),
        EeySymbol( "unknown" ) )
    init.evaluate( env )

    assert_equal( EeySymbol( "i" ).render( env ), "i" )


def test_render_simple_types():
    env = EeyEnvironment( EeyCppRenderer() )
    assert_equals( EeyType( EeyInt   ).render( env ), "int" )
    assert_equals( EeyType( EeyFloat ).render( env ), "double" )
    assert_equals( EeyType( EeyBool  ).render( env ), "bool" )
    assert_equals( EeyType( EeyVoid  ).render( env ), "void" )


def test_symbol_find_namespace_and_name():

    class MyNsHolder( object ):
        def __init__( self ):
            self.namespace = EeyNamespace()

        def evaluate( self, env ):
            return self

        def get_namespace( self ):
            return self.namespace

    env = EeyEnvironment( EeyCppRenderer() )

    a = MyNsHolder()
    env.namespace["a"] = a
    b = MyNsHolder()
    a.namespace["b"] = b

    (namespace, name, base_sym) = EeySymbol( "a.b.c" ).find_namespace_and_name(
        env )

    assert_equals( b.namespace, namespace )
    assert_equals( "c", name )
    assert_equals( "a.b", base_sym )


