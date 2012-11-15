# Copyright (C) 2011-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


from nose.tools import *

from libpepper import builtins
from libpepper.environment import PepEnvironment
from libpepper.cpp.cppvalues import *
from libpepper.cpp.cpprenderer import PepCppRenderer
from libpepper.builtinmodules.pepsys import PepSysArgv


#def test_Known_plus_string():
#    env = PepEnvironment( PepCppRenderer() )
#    env.namespace["input"] = PepVariable( PepType( PepString ), "input" )
#
#    value = PepPlus( PepString( "known" ), PepSymbol( "input" ) )
#
#    assert_equal( value.render( env ), '("known" + input)' )
#
#
#def test_Known_plus_string_inside_print():
#    env = PepEnvironment( PepCppRenderer() )
#    env.namespace["input"] = PepVariable( PepType( PepString ), "input" )
#
#    value = PepPrint( PepPlus( PepString( "known" ), PepSymbol( "input" ) ) )
#
#    assert_equal( value.render( env ), 'printf( "known%s", input )' )

def test_Known_plus_argv():
    env = PepEnvironment( PepCppRenderer() )
    builtins.add_builtins( env )

    value = PepFunctionCall( PepSymbol( "print" ), (
        PepPlus(
            PepString( "known" ),
            PepArrayLookup( PepSysArgv(), PepInt( "1" ) )
            ),
        ) )

    assert_equal( value.render( env ), 'printf( "known%s\\n", argv[1] )' )


def test_Known_plus_argv_plus_known():
    env = PepEnvironment( PepCppRenderer() )
    builtins.add_builtins( env )

    value = PepFunctionCall( PepSymbol( "print" ), (
        PepPlus(
            PepString( "known" ),
            PepPlus(
                PepArrayLookup( PepSysArgv(), PepInt( "1" ) ),
                PepString( "known2" )
                )
            ),
        ) )

    assert_equal( value.render( env ), 'printf( "known%sknown2\\n", argv[1] )' )


