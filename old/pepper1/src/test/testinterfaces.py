# Copyright (C) 2013 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

# Thus the people were divided because of Jesus.  John 4 v43

from nose.tools import *

from libpepper import builtins
from libpepper.environment import PepEnvironment
from libpepper.vals.all_values import *

def Evaluating_an_interface_gives_a_userinterface__test():
    env = PepEnvironment( None )
    useri = PepInterface(
        PepSymbol( "MyInterface" ),
        (),
        (
            PepInterfaceDef(
                PepType( PepVoid ),
                "foo",
                ()
            ),
        )
    ).evaluate( env )

    assert_equal( PepUserInterface, env.namespace["MyInterface"].__class__ )

def make_interface( env ):
    PepInterface(
        PepSymbol( "MyInterface" ),
        (),
        (
            PepInterfaceDef(
                PepType( PepInt ),
                PepSymbol( "add" ),
                (
                    ( PepType( PepInt ), PepSymbol( "a" ) ),
                    ( PepType( PepInt ), PepSymbol( "b" ) ),
                )
            ),
        )
    ).evaluate( env )
    return env.namespace["MyInterface"]

def make_matching_class( env ):
    PepClass(
        PepSymbol( "MyClass" ),
        (),
        (
            PepDef(
                PepType( PepInt ),
                PepSymbol( "add" ),
                (
                    ( PepType( PepInt ), PepSymbol( "a" ) ),
                    ( PepType( PepInt ), PepSymbol( "b" ) ),
                ),
                ( PepPass(), )
            ),
        )
    ).evaluate( env )
    return env.namespace["MyClass"]

def make_nonmatching_class( env, name="MyClass" ):
    PepClass(
        PepSymbol( name ),
        (),
        (PepPass(),)
    ).evaluate( env )
    return env.namespace[name]

def User_class_matching_interface_matches__test():
    env = PepEnvironment( None )
    myinterface = make_interface( env )
    myclass     = make_matching_class( env ).evaluate( env )
    assert_true( myinterface.can_match( myclass, env ) )

def Nonmatching_interface_doesnt_match__test():
    env = PepEnvironment( None )
    myinterface = make_interface( env )
    myclass     = make_nonmatching_class( env ).evaluate( env )
    assert_false( myinterface.can_match( myclass, env ) )


def User_class_matching_interface_call_to_matches_returns_true__test():
    env = PepEnvironment( None )
    myinterface = make_interface( env )
    myclass     = make_matching_class( env ).evaluate( env )
    ans = PepFunctionCall(
        PepSymbol( "MyInterface.matches" ),
        (
            PepSymbol( "MyClass" ),
        )
    ).evaluate( env )

    assert_equal( PepBool, ans.__class__ )
    assert_equal( True, ans.value )

def User_class_nonmatching_interface_call_to_matches_returns_false__test():
    env = PepEnvironment( None )
    myinterface = make_interface( env )
    myclass     = make_nonmatching_class( env ).evaluate( env )
    ans = PepFunctionCall(
        PepSymbol( "MyInterface.matches" ),
        (
            PepSymbol( "MyClass" ),
        )
    ).evaluate( env )

    assert_equal( PepBool, ans.__class__ )
    assert_equal( False, ans.value )



def User_class_matching_interface_call_to_implements_returns_true__test():
    env = PepEnvironment( None )
    myinterface = make_interface( env )
    myclass     = make_matching_class( env ).evaluate( env )
    ans = PepFunctionCall(
        PepSymbol( "MyClass.implements" ),
        (
            PepSymbol( "MyInterface" ),
        )
    ).evaluate( env )

    assert_equal( PepBool, ans.__class__ )
    assert_equal( True, ans.value )

def User_class_nonmatching_interface_call_to_implements_returns_false__test():
    env = PepEnvironment( None )
    myinterface = make_interface( env )
    myclass     = make_nonmatching_class( env ).evaluate( env )
    ans = PepFunctionCall(
        PepSymbol( "MyClass.implements" ),
        (
            PepSymbol( "MyInterface" ),
        )
    ).evaluate( env )

    assert_equal( PepBool, ans.__class__ )
    assert_equal( False, ans.value )

# TODO: check you can't use an interface as a param type - must be
#       wrapped by implements()

def Function_can_take_implements_MyInterface_as_param_type__test():
    env = PepEnvironment( None )
    builtins.add_builtins( env )

    nmclass     = make_nonmatching_class( env, "MyNmClass" ).evaluate( env )
    mclass      = make_matching_class( env ).evaluate( env )
    myinterface = make_interface( env ).evaluate( env )

    fn = PepUserFunction(
        "myfunc",
        PepType( PepVoid ),
        (
            (
                PepFunctionCall(
                    PepSymbol( "implements" ),
                    (PepSymbol( "MyInterface" ),)
                ),
                PepSymbol( "x" )
            ),
        ),
        (
            PepPass(),
        )
    ).evaluate( env )

    PepInit(
        PepSymbol( "MyNmClass" ),
        PepSymbol( "nm" ),
        PepFunctionCall( PepSymbol( 'MyNmClass.init' ), () )
    ).evaluate( env )

    PepInit(
        PepSymbol( "MyClass" ),
        PepSymbol( "m" ),
        PepFunctionCall( PepSymbol( 'MyClass.init' ), () )
    ).evaluate( env )

    # An instance of the non-matching class is not a valid argument
    assert_false( fn.args_match( ( PepSymbol("nm").evaluate( env ),), env ) )

    # But an instance of the matching class is
    assert_true( fn.args_match( ( PepSymbol("m").evaluate( env ),), env ) )

