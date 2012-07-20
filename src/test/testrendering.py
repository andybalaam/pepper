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
    rtfn = EeyRuntimeUserFunction( fn, (), None )

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
    rtfn1 = EeyRuntimeUserFunction( fn, (), None )
    rtfn2 = EeyRuntimeUserFunction( fn, (), None )

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

    rtfn1 = EeyRuntimeUserFunction( fnflt, ( EeyFloat( "3.0" ), ), None )
    rtfn2 = EeyRuntimeUserFunction( fnint, ( EeyInt( "3" ),     ), None )
    rtfn3 = EeyRuntimeUserFunction( fnint, ( EeyInt( "4" ),     ), None )
    rtfn4 = EeyRuntimeUserFunction( fnflt, ( EeyFloat( "5.1" ), ), None )

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

    rtfn1 = EeyRuntimeUserFunction( fnint, ( EeyInt( "3" ), ), None )
    rtfn2 = EeyRuntimeUserFunction( fnbool,
        (
            EeyGreaterThan(
                EeyVariable( EeyType( EeyInt ), "r" ),
                EeyVariable( EeyType( EeyInt ), "s" )
            ),
        ),
        None
    )

    assert_equal( env.renderer.add_function( rtfn1, env ), "myfn" )
    assert_equal( env.renderer.add_function( rtfn2, env ), "myfn_eey_1" )



def test_Render_runtime_class():
    env = EeyEnvironment( EeyCppRenderer() )
    add_builtins( env )

    env.namespace['a'] = EeyVariable( EeyType( EeyInt ), "a" )

    cls = EeyClass(
        EeySymbol( 'MyClass' ),
        (),
        (
            EeyDefInit(
                (
                    ( EeySymbol('MyClass'), EeySymbol('self') ),
                    ( EeySymbol('int'), EeySymbol('a') ),
                    ( EeySymbol('float'), EeySymbol('b') )
                ),
                (
                    EeyVar(
                        (
                            EeyInit(
                                EeySymbol('int'),
                                EeySymbol('self.a'),
                                EeySymbol('a')
                            ),
                            EeyInit(
                                EeySymbol('float'),
                                EeySymbol('self.b'),
                                EeySymbol('b')
                            )
                        )
                    ),
                )
            ),
        )
    )

    init = EeyInit(
        EeySymbol( 'MyClass' ),
        EeySymbol( 'mc' ),
        EeyFunctionCall(
            EeySymbol( 'MyClass.init' ),
            ( EeySymbol( 'a' ), EeyFloat('1.5') )
        )
    )

    ans = env.renderer.render_exe( [ cls, init ], env )

    assert_equal(
        """
struct MyClass
{
    int a;
    double b;
};

void MyClass_eey_c_eey___init__( MyClass& self, int a, double b )
{
    self.a = a;
    self.b = b;
}

int main( int argc, char* argv[] )
{
    MyClass mc; MyClass_eey_c_eey___init__( mc, a, 1.5 );

    return 0;
}
""",
        ans
    )



def test_Render_runtime_method_call():
    env = EeyEnvironment( EeyCppRenderer() )
    add_builtins( env )

    env.namespace['a'] = EeyVariable( EeyType( EeyInt ), "a" )

    cls = EeyClass(
        EeySymbol( 'MyClass' ),
        (),
        (
            EeyDefInit(
                (
                    ( EeySymbol('MyClass'), EeySymbol('self') ),
                    ( EeySymbol('int'), EeySymbol('x') ),
                ),
                ( EeyPass(), )
            ),
            EeyDef(
                EeySymbol('void'),
                EeySymbol('my_meth'),
                ( ( EeySymbol('MyClass'), EeySymbol('self') ), ),
                ( EeyPass(), )
            )
        )
    )

    init = EeyInit(
        EeySymbol( 'MyClass' ),
        EeySymbol( 'mc' ),
        EeyFunctionCall( EeySymbol( 'MyClass.init' ), ( EeySymbol( "a" ), ) )
    )

    meth = EeyFunctionCall( EeySymbol( "mc.my_meth" ), () )

    ans = env.renderer.render_exe( [ cls, init, meth ], env )

    assert_equal(
        """
struct MyClass
{
};

void MyClass_eey_c_eey___init__( MyClass& self, int x )
{
}

void MyClass_eey_c_eey_my_meth( MyClass& self )
{
}

int main( int argc, char* argv[] )
{
    MyClass mc; MyClass_eey_c_eey___init__( mc, a );
    MyClass_eey_c_eey_my_meth( mc );

    return 0;
}
""",
        ans
    )



