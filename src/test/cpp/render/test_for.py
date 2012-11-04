from test.eeyasserts import assert_multiline_equal

from libeeyore import builtins
from libeeyore.environment import EeyEnvironment
from libeeyore.cpp.cpprenderer import EeyCppRenderer

from libeeyore.vals.all_values import *

def test_Basic_int_for_loop():

    env = EeyEnvironment( EeyCppRenderer() )
    builtins.add_builtins( env )

    EeyImport( "sys" ).evaluate( env )

    stmt = EeyFor(
        EeySymbol('int'),
        EeySymbol('i'),
        EeyFunctionCall(
            EeySymbol('range'),
            (
                EeyInt('0'), 
                EeyFunctionCall(
                    EeySymbol( "len" ),
                    ( EeySymbol( "sys.argv" ), )
                ),
            )
        ),
        (
            EeyFunctionCall(
                EeySymbol('print'),
                (
                    EeySymbol('i'),
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

    env = EeyEnvironment( EeyCppRenderer() )
    builtins.add_builtins( env )

    EeyImport( "sys" ).evaluate( env )
    stmt = EeyFor(
        EeySymbol('int'),
        EeySymbol('i'),
        EeyFunctionCall(
            EeySymbol('range'),
            (
                EeyInt('10'),
                EeyFunctionCall(
                    EeySymbol( "len" ),
                    ( EeySymbol( "sys.argv" ), )
                ),
                EeyInt('3'),
            )
        ),
        (
            EeyFunctionCall(
                EeySymbol('print'),
                (
                    EeySymbol('i'),
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

