
from nose.tools import *

from libeeyore.builtins import add_builtins
from libeeyore.environment import EeyEnvironment
from libeeyore.cpp.cppvalues import *
from libeeyore.cpp.cpprenderer import EeyCppRenderer



@raises( EeyUserErrorException )
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

    value.render( env ) # should throw


@raises( EeyUserErrorException )
def test_Call_fn_with_wrong_arg_type():
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

    value = EeyFunctionCall( EeySymbol( "myfunc" ), ( EeyString( "zzz" ), ) )

    value.render( env ) # should throw


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
    env.namespace["othernum"] = EeyVariable( EeyInt )

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
    assert_equal( env.renderer.functions[0],
"""int myfunc( int x, int y )
{
    return (x + y);
}
""" )


def test_return_type_of_user_defined():
    assert_equal(
        EeyUserFunction( "f", EeyType( EeyInt ), (), ( EeyPass(), )
            ).return_type(),
        EeyInt
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

    env.namespace["othernum"] = EeyVariable( EeyInt )

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
    assert_equal( env.renderer.functions[0],
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

    env.namespace["othernum"] = EeyVariable( EeyInt )

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
    assert_equal( env.renderer.functions[0],
"""int myfunc( int x, int y )
{
    int a = x;
    return (a + y);
}
""" )


