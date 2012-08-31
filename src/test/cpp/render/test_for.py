from libeeyore import builtins
from libeeyore.environment import EeyEnvironment
from libeeyore.cpp.cpprenderer import EeyCppRenderer

from libeeyore.vals.all_values import *

def test_Basic_int_for_loop():

    env = EeyEnvironment( EeyCppRenderer() )
    builtins.add_builtins( env )

    stmt = EeyFor(
        EeySymbol('int'),
        EeySymbol('i'),
        EeyFunctionCall(
            EeySymbol('range'),
            (
                EeyInt('0'), 
                EeyInt('4')
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

    assert_equal(
        """
int main( int argc, char* argv[] )
{
    for( int i = 0; i < 4; ++i )
    {
        printf( "%d", i )
    }

    return 0;
}
""",
        ans
    )


