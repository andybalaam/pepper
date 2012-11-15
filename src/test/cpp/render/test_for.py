# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

from test.pepasserts import assert_multiline_equal

from libpepper import builtins
from libpepper.environment import PepEnvironment
from libpepper.cpp.cpprenderer import PepCppRenderer

from libpepper.vals.all_values import *

def test_Basic_int_for_loop():

    env = PepEnvironment( PepCppRenderer() )
    builtins.add_builtins( env )

    PepImport( "sys" ).evaluate( env )

    stmt = PepFor(
        PepSymbol('int'),
        PepSymbol('i'),
        PepFunctionCall(
            PepSymbol('range'),
            (
                PepInt('0'), 
                PepFunctionCall(
                    PepSymbol( "len" ),
                    ( PepSymbol( "sys.argv" ), )
                ),
            )
        ),
        (
            PepFunctionCall(
                PepSymbol('print'),
                (
                    PepSymbol('i'),
                )
            ),
        )
    )

    ans = env.renderer.render_exe( [ stmt ], env )

    assert_multiline_equal(
        """#include <stdio.h>

int main( int argc, char* argv[] )
{
    for( int i = 0; i < argc; ++i )
    {
        printf( "%d\\n", i );
    }

    return 0;
}
""",
        ans
    )




def Loop_over_range_with_nondefault_step___test():

    env = PepEnvironment( PepCppRenderer() )
    builtins.add_builtins( env )

    PepImport( "sys" ).evaluate( env )
    stmt = PepFor(
        PepSymbol('int'),
        PepSymbol('i'),
        PepFunctionCall(
            PepSymbol('range'),
            (
                PepInt('10'),
                PepFunctionCall(
                    PepSymbol( "len" ),
                    ( PepSymbol( "sys.argv" ), )
                ),
                PepInt('3'),
            )
        ),
        (
            PepFunctionCall(
                PepSymbol('print'),
                (
                    PepSymbol('i'),
                )
            ),
        )
    )

    ans = env.renderer.render_exe( [ stmt ], env )

    assert_multiline_equal(
        """#include <stdio.h>

int main( int argc, char* argv[] )
{
    for( int i = 10; i < argc; i += 3 )
    {
        printf( "%d\\n", i );
    }

    return 0;
}
""",
        ans
    )


