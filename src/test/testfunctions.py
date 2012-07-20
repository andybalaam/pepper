
from nose.tools import *

from libeeyore.builtins import add_builtins
from libeeyore.environment import EeyEnvironment
from libeeyore.cpp.cppvalues import *
from libeeyore.cpp.cpprenderer import EeyCppRenderer

from eeyasserts import assert_multiline_equal

def test_Call_fn_with_wrong_num_args():
    env = EeyEnvironment( EeyCppRenderer() )

    fndecl = EeyDef(
        EeyType( EeyInt ),
        EeySymbol( "myfunc" ),
        (
            ( EeyType( EeyInt ), EeySymbol( "x" ) ),
            ),
        (
            EeyPass(),
            )
        )

    assert_equal( fndecl.render( env ), "" )

    value = EeyFunctionCall( EeySymbol( "myfunc" ), () )

    expected_error = r"""Wrong number of arguments to function myfunc.  You supplied 0, but there should be 1."""

        # This is what we are testing: should throw as no args supplied
    assert_raises_regexp(
        EeyUserErrorException,
        expected_error,
        lambda: value.render( env )
    )


def test_Call_fn_with_wrong_arg_type():
    env = EeyEnvironment( EeyCppRenderer() )
    add_builtins( env )

    fndecl = EeyDef(
        EeyType( EeyInt ),
        EeySymbol( "myfunc" ),
        (
            ( EeyType( EeyInt ), EeySymbol( "x" ) ),
            ),
        (
            EeyPass(),
            )
        )

    assert_equal( fndecl.render( env ), "" )

    value = EeyFunctionCall( EeySymbol( "myfunc" ), ( EeyString( "zzz" ), ) )

    expected_error = (
        r"""For function 'myfunc', argument 'x' should be int, not string.""" )

        # This is what we are testing: should throw as no args supplied
    assert_raises_regexp(
        EeyUserErrorException,
        expected_error,
        lambda: value.render( env )
    )


def test_Define_and_call_fn_to_add_known_numbers():
    env = EeyEnvironment( EeyCppRenderer() )

    fndecl = EeyDef(
        EeyType( EeyInt ),
        EeySymbol( "myfunc" ),
        (
            ( EeyType( EeyInt ), EeySymbol( "x" ) ),
            ( EeyType( EeyInt ), EeySymbol( "y" ) )
            ),
        (
            EeyReturn( EeyPlus( EeySymbol( "x" ), EeySymbol( "y" ) ) ),
            )
        )

    assert_equal( fndecl.render( env ), "" )

    value = EeyFunctionCall( EeySymbol( "myfunc" ),
        ( EeyInt( "3" ), EeyInt( "4" ) ) )

    assert_equal( value.render( env ), "7" )


def test_Define_and_call_fn_to_add_unknown_numbers():
    env = EeyEnvironment( EeyCppRenderer() )
    env.namespace["othernum"] = EeyVariable( EeyType( EeyInt ), "othernum" )

    fndecl = EeyDef(
        EeyType( EeyInt ),
        EeySymbol( "myfunc" ),
        (
            ( EeyType( EeyInt ), EeySymbol( "x" ) ),
            ( EeyType( EeyInt ), EeySymbol( "y" ) )
            ),
        (
            EeyReturn( EeyPlus( EeySymbol( "x" ), EeySymbol( "y" ) ) ),
            )
        )

    assert_equal( fndecl.render( env ), "" )

    value = EeyFunctionCall( EeySymbol( "myfunc" ),
        ( EeyInt( "3" ), EeySymbol( "othernum" ) ) )

    assert_equal( value.render( env ), "myfunc( 3, othernum )" )
    assert_multiline_equal( env.renderer._functions["myfunc"].values()[0][1],
"""int myfunc( int x, int y )
{
    return (x + y);
}

""" )


def test_return_type_of_user_defined():
    assert_equal(
        EeyUserFunction( "f", EeyType( EeyInt ), (), ( EeyPass(), )
            ).return_type( None, () ),
        EeyType( EeyInt )
        )


def test_Define_and_call_fn_returning_void_known():
    env = EeyEnvironment( EeyCppRenderer() )

    fndecl = EeyDef(
        EeyType( EeyVoid ),
        EeySymbol( "myfunc" ),
        (
            ),
        (
            EeyPass(),
            )
        )

    assert_equal( fndecl.render( env ), "" )

    value = EeyFunctionCall( EeySymbol( "myfunc" ), () )

    assert_equal( value.render( env ), "" )


def test_Define_and_call_fn_returning_void_unknown():
    env = EeyEnvironment( EeyCppRenderer() )
    add_builtins( env )

    env.namespace["othernum"] = EeyVariable( EeyType( EeyInt ), "othernum" )

    fndecl = EeyDef(
        EeySymbol( "void" ),
        EeySymbol( "myfunc" ),
        (
            ( EeySymbol( "int" ), EeySymbol( "x" ) ),
            ( EeySymbol( "int" ), EeySymbol( "y" ) )
            ),
        (
            EeySymbol( "pass" ),
            )
        )

    assert_equal( fndecl.render( env ), "" )

    value = EeyFunctionCall( EeySymbol( "myfunc" ),
        ( EeyInt( "3" ), EeySymbol( "othernum" ) ) )

    assert_equal( value.render( env ), "myfunc( 3, othernum )" )
    assert_multiline_equal( env.renderer._functions["myfunc"].values()[0][1],
"""void myfunc( int x, int y )
{
}

""" )


def test_Define_and_call_multiline_known_fn():
    env = EeyEnvironment( EeyCppRenderer() )

    fndecl = EeyDef(
        EeyType( EeyInt ),
        EeySymbol( "myfunc" ),
        (
            ( EeyType( EeyInt ), EeySymbol( "x" ) ),
            ( EeyType( EeyInt ), EeySymbol( "y" ) )
            ),
        (
            EeyInit( EeyType( EeyInt ), EeySymbol( "a" ), EeySymbol( "x" ) ),
            EeyReturn( EeyPlus( EeySymbol( "a" ), EeySymbol( "y" ) ) ),
            )
        )

    assert_equal( fndecl.render( env ), "" )

    value = EeyFunctionCall( EeySymbol( "myfunc" ),
        ( EeyInt( "2" ), EeyInt( "8" ) ) )

    assert_equal( value.render( env ), "10" )



def test_Define_and_call_multiline_unknown_fn():
    env = EeyEnvironment( EeyCppRenderer() )

    env.namespace["othernum"] = EeyVariable( EeyType( EeyInt ), "othernum" )

    fndecl = EeyDef(
        EeyType( EeyInt ),
        EeySymbol( "myfunc" ),
        (
            ( EeyType( EeyInt ), EeySymbol( "x" ) ),
            ( EeyType( EeyInt ), EeySymbol( "y" ) )
            ),
        (
            EeyInit( EeyType( EeyInt ), EeySymbol( "a" ), EeySymbol( "x" ) ),
            EeyReturn( EeyPlus( EeySymbol( "a" ), EeySymbol( "y" ) ) ),
            )
        )

    assert_equal( fndecl.render( env ), "" )

    value = EeyFunctionCall( EeySymbol( "myfunc" ),
        ( EeyInt( "2" ), EeySymbol( "othernum" ) ) )

    assert_equal( value.render( env ), "myfunc( 2, othernum )" )
    assert_multiline_equal( env.renderer._functions["myfunc"].values()[0][1],
"""int myfunc( int x, int y )
{
    int a = x;
    return (a + y);
}

""" )



def test_Can_define_2_fns_with_same_name():
    env = EeyEnvironment( EeyCppRenderer() )

    fndecl1 = EeyDef(
        EeyType( EeyVoid ),
        EeySymbol( "myfunc" ),
            (
                ( EeyType( EeyInt ), EeySymbol( "x" ) ),
            ),
            (
                EeyPass(),
            )
        )

    fndecl2 = EeyDef(
        EeyType( EeyVoid ),
        EeySymbol( "myfunc" ),
            (
                ( EeyType( EeyFloat ), EeySymbol( "x" ) ),
            ),
            (
                EeyPass(),
            )
        )

    fndecl1.render( env )

     # This should not throw - we are allowed to declare a second function
     # with the same name.
    fndecl2.render( env )


def test_Call_overloaded_fn_with_wrong_arg_type():
    env = EeyEnvironment( EeyCppRenderer() )
    add_builtins( env )

    fndecl1 = EeyDef( EeyType( EeyVoid ), EeySymbol( "myfunc" ),
            (
                ( EeyType( EeyInt ), EeySymbol( "x" ) ),
            ),
            (
                EeyPass(),
            )
        )

    fndecl2 = EeyDef( EeyType( EeyVoid ), EeySymbol( "myfunc" ),
            (
                ( EeyType( EeyFloat ), EeySymbol( "x" ) ),
            ),
            (
                EeyPass(),
            )
        )

    fndecl1.render( env )
    fndecl2.render( env )

    value = EeyFunctionCall( EeySymbol( "myfunc" ), ( EeyString( "foo" ), ) )

    expected_error = r"""No overload of function myfunc matches the supplied arguments.  You supplied:
\(string foo\)
but the only allowed argument lists are:
\(int x\)
\(float x\)
"""

        # This is what we are testing: should throw as String is not allowed
    assert_raises_regexp(
        EeyUserErrorException,
        expected_error,
        lambda: value.render( env )
    )



def test_Call_overloaded_fn_with_wrong_num_args():
    env = EeyEnvironment( EeyCppRenderer() )
    add_builtins( env )

    fndecl1 = EeyDef( EeyType( EeyVoid ), EeySymbol( "myfunc" ),
            (
                ( EeyType( EeyInt ), EeySymbol( "x" ) ),
            ),
            (
                EeyPass(),
            )
        )

    fndecl2 = EeyDef( EeyType( EeyVoid ), EeySymbol( "myfunc" ),
            (
                ( EeyType( EeyFloat ), EeySymbol( "x" ) ),
                ( EeyType( EeyFloat ), EeySymbol( "y" ) ),
            ),
            (
                EeyPass(),
            )
        )

    fndecl1.render( env )
    fndecl2.render( env )

    value = EeyFunctionCall( EeySymbol( "myfunc" ), () )

    expected_error = r"""No overload of function myfunc matches the supplied arguments.  You supplied:
\(\)
but the only allowed argument lists are:
\(int x\)
\(float x, float y\)
"""

        # This is what we are testing: should throw as no args supplied
    assert_raises_regexp(
        EeyUserErrorException,
        expected_error,
        lambda: value.render( env )
    )


def test_Choose_overload_by_arg_type():
    env = EeyEnvironment( EeyCppRenderer() )

    fndecl1 = EeyDef( EeyType( EeyString ), EeySymbol( "myfunc" ),
            (
                ( EeyType( EeyString ), EeySymbol( "z" ) ),
                ( EeyType( EeyInt ), EeySymbol( "x" ) ),
            ),
            (
                EeyReturn( EeyString( "String,Int" ) ),
            )
        )

    fndecl2 = EeyDef( EeyType( EeyString ), EeySymbol( "myfunc" ),
            (
                ( EeyType( EeyString ), EeySymbol( "z" ) ),
                ( EeyType( EeyFloat ), EeySymbol( "x" ) ),
            ),
            (
                EeyReturn( EeyString( "String,Float" ) ),
            )
        )

    fndecl1.render( env )
    fndecl2.render( env )

    intvalue = EeyFunctionCall( EeySymbol( "myfunc" ),
        ( EeyString( "foo" ), EeyInt( "3" ) ) )

    floatvalue = EeyFunctionCall( EeySymbol( "myfunc" ),
        ( EeyString( "foo" ), EeyFloat( "3.2" ) ) )

    assert_equal( intvalue.render( env ), '"String,Int"' )
    assert_equal( floatvalue.render( env ), '"String,Float"' )




def test_Choose_overload_by_num_args():
    env = EeyEnvironment( EeyCppRenderer() )

    fndecl1 = EeyDef( EeyType( EeyString ), EeySymbol( "myfunc" ),
            (
                ( EeyType( EeyString ), EeySymbol( "z" ) ),
                ( EeyType( EeyInt ), EeySymbol( "x" ) ),
            ),
            (
                EeyReturn( EeyString( "String,Int" ) ),
            )
        )

    fndecl2 = EeyDef( EeyType( EeyFloat ), EeySymbol( "myfunc" ),
            (
                ( EeyType( EeyString ), EeySymbol( "z" ) ),
            ),
            (
                EeyReturn( EeyString( "String" ) ),
            )
        )

    fndecl1.render( env )
    fndecl2.render( env )

    value1 = EeyFunctionCall( EeySymbol( "myfunc" ),
        ( EeyString( "foo" ), EeyInt( "3" ) ) )

    value2 = EeyFunctionCall( EeySymbol( "myfunc" ), ( EeyString( "foo" ), ) )

    assert_equal( value1.render( env ), '"String,Int"' )
    assert_equal( value2.render( env ), '"String"' )



def test_args_match_for_calculated_type():

    env = EeyEnvironment( EeyCppRenderer() )

    env.namespace["a"] = EeyInt( "3" )
    env.namespace["b"] = EeyString( "foo" )

    fndecl = EeyUserFunction(
        "myfunc",
        EeyType( EeyVoid ),
        (
            ( EeyType( EeyInt ), EeySymbol( "x" ) ),
        ),
        (
            EeyPass(),
        )
    )

    assert_true(
        fndecl.args_match(
            (
                EeySymbol( "a" ),
            ),
            env
        )
    )

    assert_false(
        fndecl.args_match(
            (
                EeySymbol( "b" ),
            ),
            env
        )
    )


@raises( AssertionError )
def test_args_dont_match_error_when_they_do():
    env = EeyEnvironment( EeyCppRenderer() )

    env.namespace["a"] = EeyInt( "3" )

    fndecl = EeyUserFunction(
        "myfunc",
        EeyType( EeyVoid ),
        (
            ( EeyType( EeyInt ), EeySymbol( "x" ) ),
        ),
        (
            EeyPass(),
        )
    )

    overload = EeyFunctionOverloadList( [fndecl] )

    # Should throw since the args do match!
    overload.args_dont_match_error(
        fndecl,
        (
            EeySymbol( "a" ),
        ),
        env
    )

def test_Overloaded_functions_supply_correct_return_type_based_on_args():
    env = EeyEnvironment( EeyCppRenderer() )
    add_builtins( env )

    # Make a function taking ints, and another taking strings, with different
    # return types

    int_function = EeyUserFunction(
        "int_function",
        EeyType( EeyFloat ),
        (
            ( EeySymbol( "int" ), EeySymbol( "a1" ) ),
            ( EeySymbol( "int" ), EeySymbol( "a2" ) ),
        ),
        ( EeyPass(), )
    )

    string_function = EeyUserFunction(
        "string_function",
        EeyType( EeyInt ),
        (
            ( EeySymbol( "string" ), EeySymbol( "b1" ) ),
            ( EeySymbol( "string" ), EeySymbol( "b2" ) ),
        ),
        ( EeyPass(), )
    )

    # Make an overload list that consists of these 2 functions

    overload = EeyFunctionOverloadList( [ int_function, string_function ] )

    # Set up some variables to use as arguments

    env.namespace["i1"] = EeyInt( "3" )
    env.namespace["i2"] = EeyInt( "4" )
    env.namespace["s1"] = EeyString( "s1" )
    env.namespace["s2"] = EeyString( "s2" )

    s_i1 = EeySymbol( "i1" )
    s_i2 = EeySymbol( "i2" )
    s_s1 = EeySymbol( "s1" )
    s_s2 = EeySymbol( "s2" )

    # This is what we are testing: ask for the overload's return type,
    # supplying arguments to disambiguate which function we really mean

    assert_equal(
        EeyType( EeyFloat ),
        overload.return_type( ( s_i1, s_i2 ), env )
    )

    assert_equal(
        EeyType( EeyInt ),
        overload.return_type( ( s_s1, s_s2 ), env )
    )


