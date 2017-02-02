# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

from nose.tools import *

from libpepper.builtins import add_builtins
from libpepper.vals.all_values import *
from libpepper.environment import PepEnvironment
from libpepper.cpp.cpprenderer import PepCppRenderer

def Initial_optional_arg_is_used_when_missed_out___test():

    env = PepEnvironment( PepCppRenderer() )

    fndecl = PepDef(
        PepType( PepInt ),
        PepSymbol( "myfunc" ),
        (
            ( PepType( PepInt ), PepSymbol( "x" ), PepInt( "13" ) ),
        ),
        (
            PepReturn( PepSymbol( "x" ) ),
        )
    )

    fndecl.evaluate( env )

    value = PepFunctionCall( PepSymbol( "myfunc" ), () )

    assert_equal( value.render( env ), "13" )


def Initial_optional_arg_is_not_used_when_arg_is_supplied___test():

    env = PepEnvironment( PepCppRenderer() )

    fndecl = PepDef(
        PepType( PepInt ),
        PepSymbol( "myfunc" ),
        (
            ( PepType( PepInt ), PepSymbol( "x" ), PepInt( "13" ) ),
        ),
        (
            PepReturn( PepSymbol( "x" ) ),
        )
    )

    fndecl.evaluate( env )

    value = PepFunctionCall( PepSymbol( "myfunc" ), ( PepInt( "99" ), ) )

    assert_equal( value.render( env ), "99" )


def Later_optional_arg_is_used_when_missed_out___test():

    env = PepEnvironment( PepCppRenderer() )

    fndecl = PepDef(
        PepType( PepInt ),
        PepSymbol( "myfunc" ),
        (
            ( PepType( PepInt ), PepSymbol( "x" ) ),
            ( PepType( PepInt ), PepSymbol( "y" ) ),
            ( PepType( PepInt ), PepSymbol( "z" ), PepInt( "14" ) ),
        ),
        (
            PepReturn( PepSymbol( "z" ) ),
        )
    )

    fndecl.evaluate( env )

    value = PepFunctionCall(
        PepSymbol( "myfunc" ), ( PepInt( "2" ), PepInt( "1" ) )
    )

    assert_equal( value.render( env ), "14" )


def Later_optional_arg_is_not_used_when_arg_is_supplied___test():

    env = PepEnvironment( PepCppRenderer() )

    fndecl = PepDef(
        PepType( PepInt ),
        PepSymbol( "myfunc" ),
        (
            ( PepType( PepInt ), PepSymbol( "x" ) ),
            ( PepType( PepInt ), PepSymbol( "y" ) ),
            ( PepType( PepInt ), PepSymbol( "z" ), PepInt( "14" ) ),
        ),
        (
            PepReturn( PepSymbol( "z" ) ),
        )
    )

    fndecl.evaluate( env )

    value = PepFunctionCall(
        PepSymbol( "myfunc" ), ( PepInt( "2" ), PepInt( "1" ), PepInt( "101" ) )
    )

    assert_equal( value.render( env ), "101" )


def Optional_arg_of_wrong_type_is_an_error___test():
    env = PepEnvironment( PepCppRenderer() )
    add_builtins( env )

    def define_and_eval():

        fndecl = PepDef(
            PepType( PepInt ),
            PepSymbol( "myfunc" ),
            (
                ( PepType( PepInt ), PepSymbol( "x" ) ),
                ( PepType( PepInt ), PepSymbol( "y" ) ),
                ( PepType( PepInt ), PepSymbol( "z" ), PepString( "foo" ) ),
            ),
            (
                PepReturn( PepSymbol( "z" ) ),
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
        PepUserErrorException,
        expected_error,
        define_and_eval
    )


