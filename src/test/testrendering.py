from nose.tools import *

from libeeyore import builtins
from libeeyore.environment import EeyEnvironment
from libeeyore.cpp.cppvalues import *
from libeeyore.cpp.cpprenderer import EeyCppRenderer

from eeyasserts import assert_multiline_equal

def test_Hello_World():
    env = EeyEnvironment( EeyCppRenderer() )
    builtins.add_builtins( env )

    value = EeyFunctionCall( EeySymbol( "print" ),
        ( EeyString( "Hello, World!" ), ) )

    assert_equal( env.render_exe( ( value, ) ), """#include <stdio.h>

int main( int argc, char* argv[] )
{
    printf( "Hello, World!\\n" );

    return 0;
}
""" )

def test_Echo_arg1():
    env = EeyEnvironment( EeyCppRenderer() )
    builtins.add_builtins( env )

    # import sys
    #
    # def string getname( string name ):
    #     return name
    #
    # print sys.argv[1]

    impt = EeyImport( "sys" )

#    fndef = EeyDefine( EeySymbol( "getname" ),
#        EeyUserFunction(
#            "getname",
#            EeyType( EeyString ),
#            (
#                ( EeyType( EeyString ), EeySymbol( "name" ) ),
#                ),
#            (
#                EeyReturn( EeySymbol( "name" ) ),
#                )
#            )
#        )

    fncall = EeyFunctionCall( EeySymbol( "print" ),
        ( EeyArrayLookup( EeySymbol( "sys.argv" ), EeyInt( "1" ) ), ) )

    program = ( impt, fncall )

    assert_equal( env.render_exe( program ), """#include <stdio.h>

int main( int argc, char* argv[] )
{
    printf( "%s\\n", argv[1] );

    return 0;
}
""" )

def test_single_statement_if():
    env = EeyEnvironment( EeyCppRenderer() )
    builtins.add_builtins( env )

    # import sys
    #
    # if len( sys.argv ) > 1:
    #   print sys.argv[1]

    impt = EeyImport( "sys" )

    ifstmt = EeyIf(
        EeyGreaterThan(
            EeyFunctionCall(
                EeySymbol( "len" ), (
                    EeySymbol( "sys.argv" ),
                    )
                ),
            EeyInt( "1" )
            ),
            (
                EeyFunctionCall(
                    EeySymbol( "print" ), (
                        EeyArrayLookup(
                            EeySymbol( "sys.argv" ),
                            EeyInt( "1" )
                            ),
                        ),
                    ),
            ),
            None
        )

    program = ( impt, ifstmt )

    assert_multiline_equal( env.render_exe( program ), """#include <stdio.h>

int main( int argc, char* argv[] )
{
    if( (argc > 1) )
    {
        printf( "%s\\n", argv[1] );
    }

    return 0;
}
""" )



def test_Two_prints():
    env = EeyEnvironment( EeyCppRenderer() )
    builtins.add_builtins( env )

    value1 = EeyFunctionCall( EeySymbol( "print" ),
        ( EeyString( "Hello," ), ) )
    value2 = EeyFunctionCall( EeySymbol( "print" ),
        ( EeyString( "World!" ), ) )

    assert_equal( env.render_exe( ( value1, value2 ) ), """#include <stdio.h>

int main( int argc, char* argv[] )
{
    printf( "Hello,\\n" );
    printf( "World!\\n" );

    return 0;
}
""" )



def test_function_with_no_args():
    env = EeyEnvironment( EeyCppRenderer() )

    fn = EeyUserFunction( "myfn", EeyType( EeyVoid ), (), ( EeyPass(), ) )
    rtfn = EeyRuntimeUserFunction( fn, () )

    ans = env.renderer.render_exe( [rtfn], env )

    assert_multiline_equal( ans, """
void myfn()
{
}

int main( int argc, char* argv[] )
{
    myfn();

    return 0;
}
""" )



def test_function_called_twice_same_args():
    env = EeyEnvironment( EeyCppRenderer() )

    fn = EeyUserFunction( "myfn", EeyType( EeyVoid ), (), ( EeyPass(), ) )
    rtfn1 = EeyRuntimeUserFunction( fn, () )
    rtfn2 = EeyRuntimeUserFunction( fn, () )

    ans = env.renderer.render_exe( [rtfn1, rtfn2], env )

    assert_multiline_equal( ans, """
void myfn()
{
}

int main( int argc, char* argv[] )
{
    myfn();
    myfn();

    return 0;
}
""" )

# TODO: test_function_called_twice_different_args_same_effect
# TODO: test_function_called_twice_different_args_different_effect i.e. in one
#       call more args are known so you see different code rendered?  If not,
#       should fix the environment that gets passed into function body renderer.



def test_overloaded_functions():
    env = EeyEnvironment( EeyCppRenderer() )

    fnint = EeyUserFunction(
        "myfn",
        EeyType( EeyVoid ),
        ( ( EeyType( EeyInt ), EeySymbol( "x" ) ), ),
        ( EeyPass(), )
    )

    fnflt = EeyUserFunction(
        "myfn",
        EeyType( EeyVoid ),
        ( ( EeyType( EeyFloat ), EeySymbol( "f" ) ), ),
        ( EeyPass(), )
    )

    rtfn1 = EeyRuntimeUserFunction( fnflt, ( EeyFloat( "3.0" ), ) )
    rtfn2 = EeyRuntimeUserFunction( fnint, ( EeyInt( "3" ), ) )
    rtfn3 = EeyRuntimeUserFunction( fnint, ( EeyInt( "4" ), ) )
    rtfn4 = EeyRuntimeUserFunction( fnflt, ( EeyFloat( "5.1" ), ) )

    ans = env.renderer.render_exe( [rtfn1, rtfn2, rtfn3, rtfn4], env )

    assert_multiline_equal( ans, """
void myfn( double f )
{
}

void myfn_eey_1( int x )
{
}

int main( int argc, char* argv[] )
{
    myfn( 3.0 );
    myfn_eey_1( 3 );
    myfn_eey_1( 4 );
    myfn( 5.1 );

    return 0;
}
""" )



def test_Choose_runtime_overload_by_evaluated_type():

    env = EeyEnvironment( EeyCppRenderer() )

    fnint = EeyUserFunction(
        "myfn",
        EeyType( EeyVoid ),
        ( ( EeyType( EeyInt ), EeySymbol( "x" ) ), ),
        ( EeyPass(), )
    )

    fnbool = EeyUserFunction(
        "myfn",
        EeyType( EeyVoid ),
        ( ( EeyType( EeyBool ), EeySymbol( "b" ) ), ),
        ( EeyPass(), )
    )

    rtfn1 = EeyRuntimeUserFunction( fnint, ( EeyInt( "3" ), ) )
    rtfn2 = EeyRuntimeUserFunction( fnbool, (
        EeyGreaterThan(
            EeyVariable( EeyType( EeyInt ) ),
            EeyVariable( EeyType( EeyInt ) )
        ),
    ) )

    assert_equal( env.renderer.add_function( env, rtfn1 ), "myfn" )
    assert_equal( env.renderer.add_function( env, rtfn2 ), "myfn_eey_1" )




