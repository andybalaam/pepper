# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

from nose.tools import *

from libpepper import builtins
from libpepper.environment import PepEnvironment

from libpepper.vals.all_values import *


def Range_with_known_args_is_known__test():
    r = PepRange( PepInt( "3" ), PepInt( "6" ), PepInt( "2" ) )
    assert_true( r.is_known( PepEnvironment( None ) ) )



def Range_with_unknown_args_is_unknown__test():
    r = PepRange(
        PepInt( "3" ), PepVariable( PepType( PepInt ), "t" ), PepInt( "2" ) )

    assert_false( r.is_known( PepEnvironment( None ) ) )

def Range_can_be_iterated___test():
    r = PepRange( PepInt( "3" ), PepInt( "8" ), PepInt( "2" ) )

    assert_equal(
        [ "3", "5", "7" ],
        [ n.value for n in r ]
    )


class FakeStatement( PepValue ):
    def __init__( self, symbolname ):
        PepValue.__init__( self )
        self.evals = []
        self.symbolname = symbolname

    def construction_args( self ):
        return ()

    def evaluate( self, env ):
        self.evals.append( PepSymbol( self.symbolname ).evaluate( env ).value )
        return self

def Loop_through_default_range___test():

    env = PepEnvironment( None )

    loop_stmt1 = FakeStatement( "i" )
    loop_stmt2 = FakeStatement( "i" )

    stmt = PepFor(
        PepSymbol('int'),
        PepSymbol('i'),
        PepRange( PepInt('0'), PepInt('4'), PepInt('1') ),
        (
            loop_stmt1,
            loop_stmt2,
        )
    )

    stmt.evaluate( env )

    assert_equal( ["0", "1", "2", "3"], loop_stmt1.evals )
    assert_equal( ["0", "1", "2", "3"], loop_stmt2.evals )


def Loop_through_stepped_range___test():

    env = PepEnvironment( None )

    loop_stmt = FakeStatement( "k1" )

    stmt = PepFor(
        PepSymbol('int'),
        PepSymbol('k1'),
        PepRange( PepInt('0'), PepInt('4'), PepInt('2') ),
        (
            loop_stmt,
        )
    )

    stmt.evaluate( env )

    assert_equal( ["0", "2"], loop_stmt.evals )


def Loop_through_default_range_function___test():

    env = PepEnvironment( None )
    builtins.add_builtins( env )

    loop_stmt1 = FakeStatement( "i" )
    loop_stmt2 = FakeStatement( "i" )

    stmt = PepFor(
        PepSymbol('int'),
        PepSymbol('i'),
        PepFunctionCall(
            PepSymbol( 'range' ),
            ( PepInt('0'), PepInt('4'), PepInt('1') ),
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

    env = PepEnvironment( None )
    builtins.add_builtins( env )

    loop_stmt = FakeStatement( "k1" )

    stmt = PepFor(
        PepSymbol('int'),
        PepSymbol('k1'),
        PepFunctionCall(
            PepSymbol( 'range' ),
            ( PepInt('0'), PepInt('4'), PepInt('2') ),
        ),
        (
            loop_stmt,
        )
    )

    stmt.evaluate( env )

    assert_equal( ["0", "2"], loop_stmt.evals )


def While_loop___test():
    env = PepEnvironment( None )
    builtins.add_builtins( env )

    loop_stmt = FakeStatement( "k1" )

    stmt1 = PepInit(
        PepSymbol('int'),
        PepSymbol('k1'),
        PepInt('1')
    )
    stmt2 = PepWhile(
        PepLessThan( PepSymbol('k1'), PepInt('4') ),
        (
            loop_stmt,
            PepModification(
                # Note: have to use a PepVariable here to make
                # PepModification work right.  Needs more thought.
                PepSymbol('k1'),
                PepInt('1')
            ),
        )
    )

    stmt1.evaluate( env )
    stmt2.evaluate( env )

    assert_equal( ["1", "2", "3"], loop_stmt.evals )

