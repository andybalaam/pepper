
from nose.tools import *

from libeeyore.builtins import add_builtins
from libeeyore.environment import EeyEnvironment
from libeeyore.cpp.cppvalues import *
from libeeyore.cpp.cpprenderer import EeyCppRenderer

from eeyasserts import assert_multiline_equal

@raises( EeyUserErrorException ) # TODO: specific exception?
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


@raises( EeyUserErrorException ) # TODO: specific exception?
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
    assert_multiline_equal( env.renderer._functions["myfunc"].values()[0][1],
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


@raises( EeyUserErrorException ) # TODO: specific exception?
def test_Call_overloaded_fn_with_wrong_arg_type():
    env = EeyEnvironment( EeyCppRenderer() )

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

    value.render( env ) # Should throw as String is not allowed



@raises( EeyUserErrorException ) # TODO: specific exception?
def test_Call_overloaded_fn_with_wrong_num_args():
    env = EeyEnvironment( EeyCppRenderer() )

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

    value.render( env ) # Should throw as no args supplied



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



