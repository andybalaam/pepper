# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

from nose.tools import *

from libeeyore.builtins import add_builtins
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


def Optional_arg_of_wrong_type_is_an_error___test():
    env = EeyEnvironment( EeyCppRenderer() )
    add_builtins( env )

    def define_and_eval():

        fndecl = EeyDef(
            EeyType( EeyInt ),
            EeySymbol( "myfunc" ),
            (
                ( EeyType( EeyInt ), EeySymbol( "x" ) ),
                ( EeyType( EeyInt ), EeySymbol( "y" ) ),
                ( EeyType( EeyInt ), EeySymbol( "z" ), EeyString( "foo" ) ),
            ),
            (
                EeyReturn( EeySymbol( "z" ) ),
            )
        )
        fndecl.evaluate( env )

    expected_error = (
        r"""In function 'myfunc', the default for argument 'z' should be """ +
        r"""int, but it is string."""
    )

        # This is what we are testing: should throw as the default arg
        # has the wrong type
    assert_raises_regexp(
        EeyUserErrorException,
        expected_error,
        define_and_eval
    )


