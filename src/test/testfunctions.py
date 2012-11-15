# Copyright (C) 2011-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


from nose.tools import *

from libpepper.builtins import add_builtins
from libpepper.environment import PepEnvironment
from libpepper.cpp.cppvalues import *
from libpepper.cpp.cpprenderer import PepCppRenderer

from pepasserts import assert_multiline_equal

def test_Call_fn_with_wrong_num_args():
    env = PepEnvironment( PepCppRenderer() )

    fndecl = PepDef(
        PepType( PepInt ),
        PepSymbol( "myfunc" ),
        (
            ( PepType( PepInt ), PepSymbol( "x" ) ),
            ),
        (
            PepPass(),
            )
        )

    assert_equal( fndecl.render( env ), "" )

    value = PepFunctionCall( PepSymbol( "myfunc" ), () )

    expected_error = r"""Wrong number of arguments to function myfunc.  You supplied 0, but there should be 1."""

        # This is what we are testing: should throw as no args supplied
    assert_raises_regexp(
        PepUserErrorException,
        expected_error,
        lambda: value.render( env )
    )


def test_Call_fn_with_wrong_arg_type():
    env = PepEnvironment( PepCppRenderer() )
    add_builtins( env )

    fndecl = PepDef(
        PepType( PepInt ),
        PepSymbol( "myfunc" ),
        (
            ( PepType( PepInt ), PepSymbol( "x" ) ),
            ),
        (
            PepPass(),
            )
        )

    assert_equal( fndecl.render( env ), "" )

    value = PepFunctionCall( PepSymbol( "myfunc" ), ( PepString( "zzz" ), ) )

    expected_error = (
        r"""For function 'myfunc', argument 'x' should be int, not string.""" )

        # This is what we are testing: should throw as string is not int
    assert_raises_regexp(
        PepUserErrorException,
        expected_error,
        lambda: value.render( env )
    )


def test_Define_and_call_fn_to_add_known_numbers():
    env = PepEnvironment( PepCppRenderer() )

    fndecl = PepDef(
        PepType( PepInt ),
        PepSymbol( "myfunc" ),
        (
            ( PepType( PepInt ), PepSymbol( "x" ) ),
            ( PepType( PepInt ), PepSymbol( "y" ) )
            ),
        (
            PepReturn( PepPlus( PepSymbol( "x" ), PepSymbol( "y" ) ) ),
            )
        )

    assert_equal( fndecl.render( env ), "" )

    value = PepFunctionCall( PepSymbol( "myfunc" ),
        ( PepInt( "3" ), PepInt( "4" ) ) )

    assert_equal( value.render( env ), "7" )


def test_Define_and_call_fn_to_add_unknown_numbers():
    env = PepEnvironment( PepCppRenderer() )
    env.namespace["othernum"] = PepVariable( PepType( PepInt ), "othernum" )

    fndecl = PepDef(
        PepType( PepInt ),
        PepSymbol( "myfunc" ),
        (
            ( PepType( PepInt ), PepSymbol( "x" ) ),
            ( PepType( PepInt ), PepSymbol( "y" ) )
            ),
        (
            PepReturn( PepPlus( PepSymbol( "x" ), PepSymbol( "y" ) ) ),
            )
        )

    assert_equal( fndecl.render( env ), "" )

    value = PepFunctionCall( PepSymbol( "myfunc" ),
        ( PepInt( "3" ), PepSymbol( "othernum" ) ) )

    assert_equal( value.render( env ), "myfunc( 3, othernum )" )
    assert_multiline_equal( env.renderer._functions["myfunc"].values()[0][1],
"""int myfunc( int x, int y )
{
    return (x + y);
}

""" )


def test_return_type_of_user_defined():
    assert_equal(
        PepUserFunction( "f", PepType( PepInt ), (), ( PepPass(), )
            ).return_type( None, () ),
        PepType( PepInt )
        )


def test_Define_and_call_fn_returning_void_known():
    env = PepEnvironment( PepCppRenderer() )

    fndecl = PepDef(
        PepType( PepVoid ),
        PepSymbol( "myfunc" ),
        (
            ),
        (
            PepPass(),
            )
        )

    assert_equal( fndecl.render( env ), "" )

    value = PepFunctionCall( PepSymbol( "myfunc" ), () )

    assert_equal( value.render( env ), "" )


def test_Define_and_call_fn_returning_void_unknown():
    env = PepEnvironment( PepCppRenderer() )
    add_builtins( env )

    env.namespace["othernum"] = PepVariable( PepType( PepInt ), "othernum" )

    fndecl = PepDef(
        PepSymbol( "void" ),
        PepSymbol( "myfunc" ),
        (
            ( PepSymbol( "int" ), PepSymbol( "x" ) ),
            ( PepSymbol( "int" ), PepSymbol( "y" ) )
            ),
        (
            PepSymbol( "pass" ),
            )
        )

    assert_equal( fndecl.render( env ), "" )

    value = PepFunctionCall( PepSymbol( "myfunc" ),
        ( PepInt( "3" ), PepSymbol( "othernum" ) ) )

    assert_equal( value.render( env ), "myfunc( 3, othernum )" )
    assert_multiline_equal( env.renderer._functions["myfunc"].values()[0][1],
"""void myfunc( int x, int y )
{
}

""" )


def test_Define_and_call_multiline_known_fn():
    env = PepEnvironment( PepCppRenderer() )

    fndecl = PepDef(
        PepType( PepInt ),
        PepSymbol( "myfunc" ),
        (
            ( PepType( PepInt ), PepSymbol( "x" ) ),
            ( PepType( PepInt ), PepSymbol( "y" ) )
            ),
        (
            PepInit( PepType( PepInt ), PepSymbol( "a" ), PepSymbol( "x" ) ),
            PepReturn( PepPlus( PepSymbol( "a" ), PepSymbol( "y" ) ) ),
            )
        )

    assert_equal( fndecl.render( env ), "" )

    value = PepFunctionCall( PepSymbol( "myfunc" ),
        ( PepInt( "2" ), PepInt( "8" ) ) )

    assert_equal( value.render( env ), "10" )



def test_Define_and_call_multiline_unknown_fn():
    env = PepEnvironment( PepCppRenderer() )

    env.namespace["othernum"] = PepVariable( PepType( PepInt ), "othernum" )

    fndecl = PepDef(
        PepType( PepInt ),
        PepSymbol( "myfunc" ),
        (
            ( PepType( PepInt ), PepSymbol( "x" ) ),
            ( PepType( PepInt ), PepSymbol( "y" ) )
            ),
        (
            PepInit( PepType( PepInt ), PepSymbol( "a" ), PepSymbol( "x" ) ),
            PepReturn( PepPlus( PepSymbol( "a" ), PepSymbol( "y" ) ) ),
            )
        )

    assert_equal( fndecl.render( env ), "" )

    value = PepFunctionCall( PepSymbol( "myfunc" ),
        ( PepInt( "2" ), PepSymbol( "othernum" ) ) )

    assert_equal( value.render( env ), "myfunc( 2, othernum )" )
    assert_multiline_equal( env.renderer._functions["myfunc"].values()[0][1],
"""int myfunc( int x, int y )
{
    int a = x;
    return (a + y);
}

""" )



def test_Can_define_2_fns_with_same_name():
    env = PepEnvironment( PepCppRenderer() )

    fndecl1 = PepDef(
        PepType( PepVoid ),
        PepSymbol( "myfunc" ),
            (
                ( PepType( PepInt ), PepSymbol( "x" ) ),
            ),
            (
                PepPass(),
            )
        )

    fndecl2 = PepDef(
        PepType( PepVoid ),
        PepSymbol( "myfunc" ),
            (
                ( PepType( PepFloat ), PepSymbol( "x" ) ),
            ),
            (
                PepPass(),
            )
        )

    fndecl1.render( env )

     # This should not throw - we are allowed to declare a second function
     # with the same name.
    fndecl2.render( env )


def test_Call_overloaded_fn_with_wrong_arg_type():
    env = PepEnvironment( PepCppRenderer() )
    add_builtins( env )

    fndecl1 = PepDef( PepType( PepVoid ), PepSymbol( "myfunc" ),
            (
                ( PepType( PepInt ), PepSymbol( "x" ) ),
            ),
            (
                PepPass(),
            )
        )

    fndecl2 = PepDef( PepType( PepVoid ), PepSymbol( "myfunc" ),
            (
                ( PepType( PepFloat ), PepSymbol( "x" ) ),
            ),
            (
                PepPass(),
            )
        )

    fndecl1.render( env )
    fndecl2.render( env )

    value = PepFunctionCall( PepSymbol( "myfunc" ), ( PepString( "foo" ), ) )

    expected_error = r"""No overload of function myfunc matches the supplied arguments.  You supplied:
\(string foo\)
but the only allowed argument lists are:
\(int x\)
\(float x\)
"""

        # This is what we are testing: should throw as String is not allowed
    assert_raises_regexp(
        PepUserErrorException,
        expected_error,
        lambda: value.render( env )
    )



def test_Call_overloaded_fn_with_wrong_num_args():
    env = PepEnvironment( PepCppRenderer() )
    add_builtins( env )

    fndecl1 = PepDef( PepType( PepVoid ), PepSymbol( "myfunc" ),
            (
                ( PepType( PepInt ), PepSymbol( "x" ) ),
            ),
            (
                PepPass(),
            )
        )

    fndecl2 = PepDef( PepType( PepVoid ), PepSymbol( "myfunc" ),
            (
                ( PepType( PepFloat ), PepSymbol( "x" ) ),
                ( PepType( PepFloat ), PepSymbol( "y" ) ),
            ),
            (
                PepPass(),
            )
        )

    fndecl1.render( env )
    fndecl2.render( env )

    value = PepFunctionCall( PepSymbol( "myfunc" ), () )

    expected_error = r"""No overload of function myfunc matches the supplied arguments.  You supplied:
\(\)
but the only allowed argument lists are:
\(int x\)
\(float x, float y\)
"""

        # This is what we are testing: should throw as no args supplied
    assert_raises_regexp(
        PepUserErrorException,
        expected_error,
        lambda: value.render( env )
    )


def test_Choose_overload_by_arg_type():
    env = PepEnvironment( PepCppRenderer() )

    fndecl1 = PepDef( PepType( PepString ), PepSymbol( "myfunc" ),
            (
                ( PepType( PepString ), PepSymbol( "z" ) ),
                ( PepType( PepInt ), PepSymbol( "x" ) ),
            ),
            (
                PepReturn( PepString( "String,Int" ) ),
            )
        )

    fndecl2 = PepDef( PepType( PepString ), PepSymbol( "myfunc" ),
            (
                ( PepType( PepString ), PepSymbol( "z" ) ),
                ( PepType( PepFloat ), PepSymbol( "x" ) ),
            ),
            (
                PepReturn( PepString( "String,Float" ) ),
            )
        )

    fndecl1.render( env )
    fndecl2.render( env )

    intvalue = PepFunctionCall( PepSymbol( "myfunc" ),
        ( PepString( "foo" ), PepInt( "3" ) ) )

    floatvalue = PepFunctionCall( PepSymbol( "myfunc" ),
        ( PepString( "foo" ), PepFloat( "3.2" ) ) )

    assert_equal( intvalue.render( env ), '"String,Int"' )
    assert_equal( floatvalue.render( env ), '"String,Float"' )




def test_Choose_overload_by_num_args():
    env = PepEnvironment( PepCppRenderer() )

    fndecl1 = PepDef( PepType( PepString ), PepSymbol( "myfunc" ),
            (
                ( PepType( PepString ), PepSymbol( "z" ) ),
                ( PepType( PepInt ), PepSymbol( "x" ) ),
            ),
            (
                PepReturn( PepString( "String,Int" ) ),
            )
        )

    fndecl2 = PepDef( PepType( PepFloat ), PepSymbol( "myfunc" ),
            (
                ( PepType( PepString ), PepSymbol( "z" ) ),
            ),
            (
                PepReturn( PepString( "String" ) ),
            )
        )

    fndecl1.render( env )
    fndecl2.render( env )

    value1 = PepFunctionCall( PepSymbol( "myfunc" ),
        ( PepString( "foo" ), PepInt( "3" ) ) )

    value2 = PepFunctionCall( PepSymbol( "myfunc" ), ( PepString( "foo" ), ) )

    assert_equal( value1.render( env ), '"String,Int"' )
    assert_equal( value2.render( env ), '"String"' )



def test_args_match_for_calculated_type():

    env = PepEnvironment( PepCppRenderer() )

    env.namespace["a"] = PepInt( "3" )
    env.namespace["b"] = PepString( "foo" )

    fndecl = PepUserFunction(
        "myfunc",
        PepType( PepVoid ),
        (
            ( PepType( PepInt ), PepSymbol( "x" ) ),
        ),
        (
            PepPass(),
        )
    )

    assert_true(
        fndecl.args_match(
            (
                PepSymbol( "a" ),
            ),
            env
        )
    )

    assert_false(
        fndecl.args_match(
            (
                PepSymbol( "b" ),
            ),
            env
        )
    )


@raises( AssertionError )
def test_args_dont_match_error_when_they_do():
    env = PepEnvironment( PepCppRenderer() )

    env.namespace["a"] = PepInt( "3" )

    fndecl = PepUserFunction(
        "myfunc",
        PepType( PepVoid ),
        (
            ( PepType( PepInt ), PepSymbol( "x" ) ),
        ),
        (
            PepPass(),
        )
    )

    overload = PepFunctionOverloadList( [fndecl] )

    # Should throw since the args do match!
    overload.args_dont_match_error(
        fndecl,
        (
            PepSymbol( "a" ),
        ),
        env
    )

def test_Overloaded_functions_supply_correct_return_type_based_on_args():
    env = PepEnvironment( PepCppRenderer() )
    add_builtins( env )

    # Make a function taking ints, and another taking strings, with different
    # return types

    int_function = PepUserFunction(
        "int_function",
        PepType( PepFloat ),
        (
            ( PepSymbol( "int" ), PepSymbol( "a1" ) ),
            ( PepSymbol( "int" ), PepSymbol( "a2" ) ),
        ),
        ( PepPass(), )
    )

    string_function = PepUserFunction(
        "string_function",
        PepType( PepInt ),
        (
            ( PepSymbol( "string" ), PepSymbol( "b1" ) ),
            ( PepSymbol( "string" ), PepSymbol( "b2" ) ),
        ),
        ( PepPass(), )
    )

    # Make an overload list that consists of these 2 functions

    overload = PepFunctionOverloadList( [ int_function, string_function ] )

    # Set up some variables to use as arguments

    env.namespace["i1"] = PepInt( "3" )
    env.namespace["i2"] = PepInt( "4" )
    env.namespace["s1"] = PepString( "s1" )
    env.namespace["s2"] = PepString( "s2" )

    s_i1 = PepSymbol( "i1" )
    s_i2 = PepSymbol( "i2" )
    s_s1 = PepSymbol( "s1" )
    s_s2 = PepSymbol( "s2" )

    # This is what we are testing: ask for the overload's return type,
    # supplying arguments to disambiguate which function we really mean

    assert_equal(
        PepType( PepFloat ),
        overload.return_type( ( s_i1, s_i2 ), env )
    )

    assert_equal(
        PepType( PepInt ),
        overload.return_type( ( s_s1, s_s2 ), env )
    )


