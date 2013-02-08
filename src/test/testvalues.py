# Copyright (C) 2011-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


from nose.tools import *

from libpepper import builtins
from libpepper.environment import PepEnvironment
from libpepper.namespace import PepNamespace
from libpepper.cpp.cppvalues import *
from libpepper.cpp.cpprenderer import PepCppRenderer

def test_Const_int_value_renders_as_a_number():
    env = PepEnvironment( PepCppRenderer() )
    value = PepInt( "23" )

    assert_equal( value.render( env ), "23" )

def test_Const_float_value_renders_as_a_number():
    env = PepEnvironment( PepCppRenderer() )
    value = PepFloat( "23.65" )

    assert_equal( value.render( env ), "23.65" )



def test_Const_string_value_renders_as_a_string():
    env = PepEnvironment( PepCppRenderer() )
    value = PepString( "foo" )

    assert_equal( value.render( env ), '"foo"' )


def test_Variable_referring_to_known_int_renders_like_an_int():
    env = PepEnvironment( PepCppRenderer() )
    env.namespace["myvariable"] = PepInt( "23" )

    value = PepSymbol( "myvariable" )

    assert_equal( value.render( env ), "23" )


def test_Variable_in_subnamespace_is_found():

    # Something with a "namespace" member.  In real life, this would
    # be an PepUserClass or similar.
    class NsHolder( PepValue ):
        def __init__( self ):
            PepValue.__init__( self )
            self.namespace = PepNamespace()
        def construction_args( self ):
            return ()
        def get_namespace( self ):
            return self.namespace

    nsholder = NsHolder()

    basens = PepNamespace()
    basens["MyHolder"] = nsholder

    env = PepEnvironment( PepCppRenderer(), basens )

    nsholder.namespace["myheld"] = PepInt( "355" )

    value = PepSymbol( "MyHolder.myheld" )

    assert_equal( value.render( env ), "355" )



def test_Subnamespace_referred_by_symbol_is_found():

    # Something with a "namespace" member.  In real life, this would
    # be an PepUserClass or similar.
    class NsHolder( PepValue ):
        def __init__( self ):
            PepValue.__init__( self )
            self.namespace = PepNamespace()
        def get_namespace( self ):
            return self.namespace

        def construction_args( self ):
            return ()

    nsholder = NsHolder()

    basens = PepNamespace()
    basens["MyHolder"] = nsholder
    basens["RefHolder"] = PepSymbol( "MyHolder" )

    env = PepEnvironment( PepCppRenderer(), basens )

    nsholder.namespace["myheld"] = PepInt( "356" )

    value = PepSymbol( "RefHolder.myheld" )

    assert_equal( value.render( env ), "356" )



def test_Add_two_known_ints_renders_calculated_sum():
    env = PepEnvironment( PepCppRenderer() )
    value = PepPlus( PepInt( "2" ), PepInt( "3" ) )

    assert_equal( value.render( env ), "5" )

def test_Add_two_known_floats_renders_calculated_sum():
    env = PepEnvironment( PepCppRenderer() )
    value = PepPlus( PepFloat( "2.9" ), PepFloat( "3.1" ) )

    assert_equal( value.render( env ), "6.0" )


def test_Unknown_variable_renders_as_symbol():
    env = PepEnvironment( PepCppRenderer() )
    env.namespace["myvariable"] = PepVariable( PepType( PepInt ), "myvariable" )

    value = PepSymbol( "myvariable" )

    assert_equal( value.render( env ), "myvariable" )

def test_Add_Unknown_to_known_literal_renders_uncalculated_sum():
    env = PepEnvironment( PepCppRenderer() )
    env.namespace["input"] = PepVariable( PepType( PepInt ), "input" )

    value = PepPlus( PepInt( "4" ), PepSymbol( "input" ) )

    assert_equal( value.render( env ), "(4 + input)" )

def test_Add_Unknown_to_known_symbol_renders_uncalculated_sum():
    env = PepEnvironment( PepCppRenderer() )
    env.namespace["input"] = PepVariable( PepType( PepInt ), "input" )
    env.namespace["four"] = PepInt( "4" )

    value = PepPlus( PepSymbol( "input" ), PepSymbol( "four" ) )

    assert_equal( value.render( env ), "(input + 4)" )


def test_Unknown_inside_nested_plus_causes_whole_sum_to_be_uncalculated():
    env = PepEnvironment( PepCppRenderer() )
    env.namespace["input"] = PepVariable( PepType( PepInt ), "input" )

    value = PepPlus( PepInt( "4" ),
        PepPlus( PepInt( "5" ), PepSymbol( "input" ) ) )

    assert_equal( value.render( env ), "(4 + (5 + input))" )


def test_Print_string_renders_as_printf():
    env = PepEnvironment( PepCppRenderer() )
    builtins.add_builtins( env )

    value = PepFunctionCall( PepSymbol( "print" ),
        ( PepString( "hello" ), ) )

    assert_equal( value.render( env ), 'printf( "hello\\n" )' )
    assert_equal( env.renderer._headers, [ "stdio.h" ] )


def test_Print_unknown_int_renders_as_percent_d():
    env = PepEnvironment( PepCppRenderer() )
    builtins.add_builtins( env )

    init = PepInit(
        PepType( PepInt ),
        PepSymbol( "i" ),
        PepVariable( PepType( PepInt ), "i" )
    )

    init.evaluate( env )

    value = PepFunctionCall( PepSymbol( "print" ),
        ( PepSymbol( "i" ), ) )

    assert_equal( value.render( env ), 'printf( "%d\\n", i )' )


def test_Print_unknown_float_renders_as_percent_f():
    env = PepEnvironment( PepCppRenderer() )
    builtins.add_builtins( env )

    init = PepInit(
        PepType( PepFloat ), PepSymbol( "f" ),
        PepVariable( PepType( PepFloat ), "f" )
    )

    init.evaluate( env )

    value = PepFunctionCall( PepSymbol( "print" ),
        ( PepSymbol( "f" ), ) )

    assert_equal( value.render( env ), 'printf( "%f\\n", f )' )



def test_Print_unknown_bool_renders_as_percent_s_colon_op():
    env = PepEnvironment( PepCppRenderer() )
    builtins.add_builtins( env )

    init = PepInit(
        PepType( PepBool ), PepSymbol( "b" ),
        PepVariable( PepType( PepBool ), "b" )
    )

    init.evaluate( env )

    value = PepFunctionCall( PepSymbol( "print" ),
        ( PepSymbol( "b" ), ) )

    assert_equal(
        value.render( env ),
        'printf( "%s\\n", (b ? "True" : "False") )' )




def test_known_array_lookup():
    env = PepEnvironment( PepCppRenderer() )

    # int[] myarr = [3,4,5]
    # myarr[1]

    env.namespace["myarr"] = PepArray( PepType( PepInt ), (
        PepInt( "3" ), PepInt( "4" ), PepInt( "5" ), ) )

    value = PepArrayLookup( PepSymbol( "myarr" ), PepInt( "1" ) )

    assert_equal( value.render( env ), "4" )

def test_bool_true():
    env = PepEnvironment( PepCppRenderer() )
    value = PepBool( True )
    assert_equal( value.render( env ), "true" )

def test_bool_false():
    env = PepEnvironment( PepCppRenderer() )
    value = PepBool( False )
    assert_equal( value.render( env ), "false" )

@raises( PepInitialisingWithWrongType )
def test_initialisation_wrong_type():
    env = PepEnvironment( None )
    add_builtins( env )
    init = PepInit( PepSymbol( "int" ), PepSymbol( "i" ), PepString( "foo" ) )
    init.evaluate( env )


def test_known_initialisation_renders_nothing():
    env = PepEnvironment( PepCppRenderer() )
    add_builtins( env )
    init = PepInit( PepSymbol( "int" ), PepSymbol( "i" ), PepInt( "4" ) )
    assert_equal( init.render( env ), "" )

def test_unknown_initialisation_evaluates_to_self():
    env = PepEnvironment( PepCppRenderer() )
    add_builtins( env )
    env.namespace["unknown"] = PepVariable( PepType( PepInt ), "unknown" )
    init = PepInit( PepSymbol( "int" ), PepSymbol( "i" ),
        PepSymbol( "unknown" ) )
    assert_equal( init.evaluate( env ), init )

def test_unknown_initialisation_renders():
    env = PepEnvironment( PepCppRenderer() )
    add_builtins( env )
    env.namespace["unknown"] = PepVariable( PepType( PepInt ), "unknown" )
    init = PepInit( PepSymbol( "int" ), PepSymbol( "i" ),
        PepSymbol( "unknown" ) )
    assert_equal( init.render( env ), "int i = unknown" )


def test_unknown_initialisation_makes_symbol_valid():
    env = PepEnvironment( PepCppRenderer() )
    add_builtins( env )

    env.namespace["unknown"] = PepVariable( PepType( PepInt ), "unknown" )

    init = PepInit( PepSymbol( "int" ), PepSymbol( "i" ),
        PepSymbol( "unknown" ) )
    init.evaluate( env )

    assert_equal( PepSymbol( "i" ).render( env ), "i" )


def test_render_simple_types():
    env = PepEnvironment( PepCppRenderer() )
    assert_equals( PepType( PepInt   ).render( env ), "int" )
    assert_equals( PepType( PepFloat ).render( env ), "double" )
    assert_equals( PepType( PepBool  ).render( env ), "bool" )
    assert_equals( PepType( PepVoid  ).render( env ), "void" )


def test_symbol_find_namespace_and_name():

    class MyNsHolder( object ):
        def __init__( self ):
            self.namespace = PepNamespace()

        def evaluate( self, env ):
            return self

        def get_namespace( self ):
            return self.namespace

    env = PepEnvironment( PepCppRenderer() )

    a = MyNsHolder()
    env.namespace["a"] = a
    b = MyNsHolder()
    a.namespace["b"] = b

    (namespace, name, base_sym) = PepSymbol( "a.b.c" ).find_namespace_and_name(
        env )

    assert_equals( b.namespace, namespace )
    assert_equals( "c", name )
    assert_equals( "a.b", base_sym )


