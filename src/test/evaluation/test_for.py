# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

from nose.tools import *

from libpepper import builtins
from libpepper.environment import EeyEnvironment

from libpepper.vals.all_values import *


def Range_with_known_args_is_known__test():
    r = EeyRange( EeyInt( "3" ), EeyInt( "6" ), EeyInt( "2" ) )
    assert_true( r.is_known( EeyEnvironment( None ) ) )



def Range_with_unknown_args_is_unknown__test():
    r = EeyRange(
        EeyInt( "3" ), EeyVariable( EeyType( EeyInt ), "t" ), EeyInt( "2" ) )

    assert_false( r.is_known( EeyEnvironment( None ) ) )

def Range_can_be_iterated___test():
    r = EeyRange( EeyInt( "3" ), EeyInt( "8" ), EeyInt( "2" ) )

    assert_equal(
        [ "3", "5", "7" ],
        [ n.value for n in r ]
    )


class FakeStatement( EeyValue ):
    def __init__( self, symbolname ):
        EeyValue.__init__( self )
        self.evals = []
        self.symbolname = symbolname

    def construction_args( self ):
        return ()

    def evaluate( self, env ):
        self.evals.append( EeySymbol( self.symbolname ).evaluate( env ).value )
        return self

def Loop_through_default_range___test():

    env = EeyEnvironment( None )

    loop_stmt1 = FakeStatement( "i" )
    loop_stmt2 = FakeStatement( "i" )

    stmt = EeyFor(
        EeySymbol('int'),
        EeySymbol('i'),
        EeyRange( EeyInt('0'), EeyInt('4'), EeyInt('1') ),
        (
            loop_stmt1,
            loop_stmt2,
        )
    )

    stmt.evaluate( env )

    assert_equal( ["0", "1", "2", "3"], loop_stmt1.evals )
    assert_equal( ["0", "1", "2", "3"], loop_stmt2.evals )


def Loop_through_stepped_range___test():

    env = EeyEnvironment( None )

    loop_stmt = FakeStatement( "k1" )

    stmt = EeyFor(
        EeySymbol('int'),
        EeySymbol('k1'),
        EeyRange( EeyInt('0'), EeyInt('4'), EeyInt('2') ),
        (
            loop_stmt,
        )
    )

    stmt.evaluate( env )

    assert_equal( ["0", "2"], loop_stmt.evals )


def Loop_through_default_range_function___test():

    env = EeyEnvironment( None )
    builtins.add_builtins( env )

    loop_stmt1 = FakeStatement( "i" )
    loop_stmt2 = FakeStatement( "i" )

    stmt = EeyFor(
        EeySymbol('int'),
        EeySymbol('i'),
        EeyFunctionCall(
            EeySymbol( 'range' ),
            ( EeyInt('0'), EeyInt('4'), EeyInt('1') ),
        ),
        (
            loop_stmt1,
            loop_stmt2,
        )
    )

    stmt.evaluate( env )

    assert_equal( ["0", "1", "2", "3"], loop_stmt1.evals )
    assert_equal( ["0", "1", "2", "3"], loop_stmt2.evals )


def Loop_through_stepped_range_function___test():

    env = EeyEnvironment( None )
    builtins.add_builtins( env )

    loop_stmt = FakeStatement( "k1" )

    stmt = EeyFor(
        EeySymbol('int'),
        EeySymbol('k1'),
        EeyFunctionCall(
            EeySymbol( 'range' ),
            ( EeyInt('0'), EeyInt('4'), EeyInt('2') ),
        ),
        (
            loop_stmt,
        )
    )

    stmt.evaluate( env )

    assert_equal( ["0", "2"], loop_stmt.evals )

