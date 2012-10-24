from nose.tools import *

from libeeyore.vals.all_values import *
from libeeyore.environment import EeyEnvironment
from libeeyore.cpp.cpprenderer import EeyCppRenderer

def Initial_optional_arg_is_used_when_missed_out___test():

    env = EeyEnvironment( EeyCppRenderer() )

    fndecl = EeyDef(
        EeyType( EeyInt ),
        EeySymbol( "myfunc" ),
        (
            ( EeyType( EeyInt ), EeySymbol( "x" ), EeyInt( "13" ) ),
        ),
        (
            EeyReturn( EeySymbol( "x" ) ),
        )
    )

    fndecl.evaluate( env )

    value = EeyFunctionCall( EeySymbol( "myfunc" ), () )

    assert_equal( value.render( env ), "13" )


def Initial_optional_arg_is_not_used_when_arg_is_supplied___test():

    env = EeyEnvironment( EeyCppRenderer() )

    fndecl = EeyDef(
        EeyType( EeyInt ),
        EeySymbol( "myfunc" ),
        (
            ( EeyType( EeyInt ), EeySymbol( "x" ), EeyInt( "13" ) ),
        ),
        (
            EeyReturn( EeySymbol( "x" ) ),
        )
    )

    fndecl.evaluate( env )

    value = EeyFunctionCall( EeySymbol( "myfunc" ), ( EeyInt( "99" ), ) )

    assert_equal( value.render( env ), "99" )


def Later_optional_arg_is_used_when_missed_out___test():

    env = EeyEnvironment( EeyCppRenderer() )

    fndecl = EeyDef(
        EeyType( EeyInt ),
        EeySymbol( "myfunc" ),
        (
            ( EeyType( EeyInt ), EeySymbol( "x" ) ),
            ( EeyType( EeyInt ), EeySymbol( "y" ) ),
            ( EeyType( EeyInt ), EeySymbol( "z" ), EeyInt( "14" ) ),
        ),
        (
            EeyReturn( EeySymbol( "z" ) ),
        )
    )

    fndecl.evaluate( env )

    value = EeyFunctionCall(
        EeySymbol( "myfunc" ), ( EeyInt( "2" ), EeyInt( "1" ) )
    )

    assert_equal( value.render( env ), "14" )


def Later_optional_arg_is_not_used_when_arg_is_supplied___test():

    env = EeyEnvironment( EeyCppRenderer() )

    fndecl = EeyDef(
        EeyType( EeyInt ),
        EeySymbol( "myfunc" ),
        (
            ( EeyType( EeyInt ), EeySymbol( "x" ) ),
            ( EeyType( EeyInt ), EeySymbol( "y" ) ),
            ( EeyType( EeyInt ), EeySymbol( "z" ), EeyInt( "14" ) ),
        ),
        (
            EeyReturn( EeySymbol( "z" ) ),
        )
    )

    fndecl.evaluate( env )

    value = EeyFunctionCall(
        EeySymbol( "myfunc" ), ( EeyInt( "2" ), EeyInt( "1" ), EeyInt( "101" ) )
    )

    assert_equal( value.render( env ), "101" )


