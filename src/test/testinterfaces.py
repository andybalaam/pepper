# Copyright (C) 2013 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

# Thus the people were divided because of Jesus.  John 4 v43

from nose.tools import *

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

def make_nonmatching_class( env ):
    PepClass(
        PepSymbol( "MyClass" ),
        (),
        (PepPass(),)
    ).evaluate( env )
    return env.namespace["MyClass"]

def User_class_matching_interface_matches__test():
    env = PepEnvironment( None )
    myinterface = make_interface( env )
    myclass     = make_matching_class( env ).evaluate( env )
    assert_true( myinterface.can_match( myclass ) )

def Nonmatching_interface_doesnt_match__test():
    env = PepEnvironment( None )
    myinterface = make_interface( env )
    myclass     = make_nonmatching_class( env ).evaluate( env )
    assert_false( myinterface.can_match( myclass ) )


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





