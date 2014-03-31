# Copyright (C) 2011-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

from nose.tools import *

from libpepper import builtins
from libpepper.environment import PepEnvironment
from libpepper.cpp.cppvalues import *
from libpepper.cpp.cpprenderer import PepCppRenderer

from libpepper.vals.all_values import *

from pepasserts import assert_multiline_equal
from asserts import assert_rendered_cpp_equals
from asserts import assert_rendered_program_equals

def test_Hello_World():
    env = PepEnvironment( PepCppRenderer() )
    builtins.add_builtins( env )

    value = PepFunctionCall( PepSymbol( "print" ),
        ( PepString( "Hello, World!" ), ) )

    assert_multiline_equal(
        env.render_exe( ( value, ) ),
        """#include <stdio.h>

int main( int argc, char* argv[] )
{
    printf( "Hello, World!\\n" );

    return 0;
}
""" )

def test_Echo_arg1():
    env = PepEnvironment( PepCppRenderer() )
    builtins.add_builtins( env )

    # import sys
    #
    # def string getname( string name ):
    #     return name
    #
    # print sys.argv[1]

    impt = PepImport( "sys" )

#    fndef = PepDefine( PepSymbol( "getname" ),
#        PepUserFunction(
#            "getname",
#            PepType( PepString ),
#            (
#                ( PepType( PepString ), PepSymbol( "name" ) ),
#                ),
#            (
#                PepReturn( PepSymbol( "name" ) ),
#                )
#            )
#        )

    fncall = PepFunctionCall( PepSymbol( "print" ),
        ( PepArrayLookup( PepSymbol( "sys.argv" ), PepInt( "1" ) ), ) )

    program = ( impt, fncall )

    assert_multiline_equal(
        env.render_exe( program ),
        """#include <stdio.h>

int main( int argc, char* argv[] )
{
    printf( "%s\\n", argv[1] );

    return 0;
}
""" )

def test_single_statement_if():
    env = PepEnvironment( PepCppRenderer() )
    builtins.add_builtins( env )

    # import sys
    #
    # if len( sys.argv ) > 1:
    #   print sys.argv[1]

    impt = PepImport( "sys" )

    ifstmt = PepIf(
        PepGreaterThan(
            PepFunctionCall(
                PepSymbol( "len" ), (
                    PepSymbol( "sys.argv" ),
                    )
                ),
            PepInt( "1" )
            ),
            (
                PepFunctionCall(
                    PepSymbol( "print" ), (
                        PepArrayLookup(
                            PepSymbol( "sys.argv" ),
                            PepInt( "1" )
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

# TODO: fails - symbols need to be not evaluated,
# but this breaks a lot of other stuff at the moment.
#def While_renders__test():
#    assert_rendered_program_equals(
#        r"""#include <stdio.h>
#
#int main( int argc, char* argv[] )
#{
#    int i = 0;
#    while( ( i < 10 ) )
#    {
#        printf( "%d\\n", i );
#    }
#
#    return 0;
#}
#""",
#        """
#int i = 0
#while i < 10:
#    print( i )
#"""
#)
#


def Less_than_renders_in_cpp__test():
    env = PepEnvironment( PepCppRenderer() )
    assert_equal(
        "(3 < 4)",
        PepLessThan( PepInt("3"), PepInt("4" ) ).render( env )
    )


def test_Two_prints():
    env = PepEnvironment( PepCppRenderer() )
    builtins.add_builtins( env )

    value1 = PepFunctionCall( PepSymbol( "print" ),
        ( PepString( "Hello," ), ) )
    value2 = PepFunctionCall( PepSymbol( "print" ),
        ( PepString( "World!" ), ) )

    assert_multiline_equal(
        env.render_exe( ( value1, value2 ) ),
        """#include <stdio.h>

int main( int argc, char* argv[] )
{
    printf( "Hello,\\n" );
    printf( "World!\\n" );

    return 0;
}
""" )



def test_function_with_no_args():
    env = PepEnvironment( PepCppRenderer() )

    fn = PepUserFunction( "myfn", PepType( PepVoid ), (), ( PepPass(), ) )
    rtfn = PepRuntimeUserFunction( fn, (), None )

    ans = env.renderer.render_exe( [rtfn], env )

    assert_multiline_equal( ans, """
void myfn();

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
    env = PepEnvironment( PepCppRenderer() )

    fn = PepUserFunction( "myfn", PepType( PepVoid ), (), ( PepPass(), ) )
    rtfn1 = PepRuntimeUserFunction( fn, (), None )
    rtfn2 = PepRuntimeUserFunction( fn, (), None )

    ans = env.renderer.render_exe( [rtfn1, rtfn2], env )

    assert_multiline_equal( ans, """
void myfn();

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
    env = PepEnvironment( PepCppRenderer() )

    fnint = PepUserFunction(
        "myfn",
        PepType( PepVoid ),
        ( ( PepType( PepInt ), PepSymbol( "x" ) ), ),
        ( PepPass(), )
    )

    fnflt = PepUserFunction(
        "myfn",
        PepType( PepVoid ),
        ( ( PepType( PepFloat ), PepSymbol( "f" ) ), ),
        ( PepPass(), )
    )

    rtfn1 = PepRuntimeUserFunction( fnflt, ( PepFloat( "3.0" ), ), None )
    rtfn2 = PepRuntimeUserFunction( fnint, ( PepInt( "3" ),     ), None )
    rtfn3 = PepRuntimeUserFunction( fnint, ( PepInt( "4" ),     ), None )
    rtfn4 = PepRuntimeUserFunction( fnflt, ( PepFloat( "5.1" ), ), None )

    ans = env.renderer.render_exe( [rtfn1, rtfn2, rtfn3, rtfn4], env )

    assert_multiline_equal( ans, """
void myfn( double f );
void myfn_pep_1( int x );

void myfn( double f )
{
}

void myfn_pep_1( int x )
{
}

int main( int argc, char* argv[] )
{
    myfn( 3.0 );
    myfn_pep_1( 3 );
    myfn_pep_1( 4 );
    myfn( 5.1 );

    return 0;
}
""" )



def test_Choose_runtime_overload_by_evaluated_type():

    env = PepEnvironment( PepCppRenderer() )

    fnint = PepUserFunction(
        "myfn",
        PepType( PepVoid ),
        ( ( PepType( PepInt ), PepSymbol( "x" ) ), ),
        ( PepPass(), )
    )

    fnbool = PepUserFunction(
        "myfn",
        PepType( PepVoid ),
        ( ( PepType( PepBool ), PepSymbol( "b" ) ), ),
        ( PepPass(), )
    )

    rtfn1 = PepRuntimeUserFunction( fnint, ( PepInt( "3" ), ), None )
    rtfn2 = PepRuntimeUserFunction( fnbool,
        (
            PepGreaterThan(
                PepVariable( PepType( PepInt ), "r" ),
                PepVariable( PepType( PepInt ), "s" )
            ),
        ),
        None
    )

    assert_equal( env.renderer.add_function( rtfn1, env ), "myfn" )
    assert_equal( env.renderer.add_function( rtfn2, env ), "myfn_pep_1" )



def test_Render_runtime_class():
    env = PepEnvironment( PepCppRenderer() )
    add_builtins( env )

    env.namespace['a'] = PepVariable( PepType( PepInt ), "a" )

    cls = PepClass(
        PepSymbol( 'MyClass' ),
        (),
        (
            PepDefInit(
                (
                    ( PepSymbol('MyClass'), PepSymbol('self') ),
                    ( PepSymbol('int'), PepSymbol('a') ),
                    ( PepSymbol('float'), PepSymbol('b') )
                ),
                (
                    PepVar(
                        (
                            PepInit(
                                PepSymbol('int'),
                                PepSymbol('self.a'),
                                PepSymbol('a')
                            ),
                            PepInit(
                                PepSymbol('float'),
                                PepSymbol('self.b'),
                                PepSymbol('b')
                            )
                        )
                    ),
                )
            ),
        )
    ).evaluate( env )

    init = PepInit(
        PepSymbol( 'MyClass' ),
        PepSymbol( 'mc' ),
        PepFunctionCall(
            PepSymbol( 'MyClass.init' ),
            ( PepSymbol( 'a' ), PepFloat('1.5') )
        )
    ).evaluate( env )

    ans = env.renderer.render_exe( [ cls, init ], env )

    assert_multiline_equal(
        """
struct MyClass
{
    int a;
    double b;
};

void MyClass_pep_c_pep___init__( MyClass& self, int a, double b );

void MyClass_pep_c_pep___init__( MyClass& self, int a, double b )
{
    self.a = a;
    self.b = b;
}

int main( int argc, char* argv[] )
{
    MyClass mc; MyClass_pep_c_pep___init__( mc, a, 1.5 );

    return 0;
}
""",
        ans
    )



def test_Render_runtime_method_call():
    env = PepEnvironment( PepCppRenderer() )
    add_builtins( env )

    env.namespace['a'] = PepVariable( PepType( PepInt ), "a" )

    cls = PepClass(
        PepSymbol( 'MyClass' ),
        (),
        (
            PepDefInit(
                (
                    ( PepSymbol('MyClass'), PepSymbol('self') ),
                    ( PepSymbol('int'), PepSymbol('x') ),
                ),
                ( PepPass(), )
            ),
            PepDef(
                PepSymbol('void'),
                PepSymbol('my_meth'),
                ( ( PepSymbol('MyClass'), PepSymbol('self') ), ),
                ( PepPass(), )
            )
        )
    ).evaluate( env )

    init = PepInit(
        PepSymbol( 'MyClass' ),
        PepSymbol( 'mc' ),
        PepFunctionCall( PepSymbol( 'MyClass.init' ), ( PepSymbol( "a" ), ) )
    ).evaluate( env )

    meth = PepFunctionCall( PepSymbol( "mc.my_meth" ), () ).evaluate( env )

    ans = env.renderer.render_exe( [ cls, init, meth ], env )

    assert_multiline_equal(
        """
struct MyClass
{
};

void MyClass_pep_c_pep_my_meth( MyClass& self );
void MyClass_pep_c_pep___init__( MyClass& self, int x );

void MyClass_pep_c_pep_my_meth( MyClass& self )
{
}

void MyClass_pep_c_pep___init__( MyClass& self, int x )
{
}

int main( int argc, char* argv[] )
{
    MyClass mc; MyClass_pep_c_pep___init__( mc, a );
    MyClass_pep_c_pep_my_meth( mc );

    return 0;
}
""",
        ans
    )


def Can_render_function_type_as_a_function_pointer__test():
    assert_rendered_cpp_equals(
        "int (*)( double, double )",
        "function( int, ( float, float ) )"
    )

def Can_render_function_returning_function__test():
    assert_rendered_program_equals(
        """
void (*get_fn( int unused ))( int, int );
void myfn( int unused, int i );

void (*get_fn( int unused ))( int, int )
{
    return myfn;
}

void myfn( int unused, int i )
{
}

int main( int argc, char* argv[] )
{
    void (*got_fn)( int, int ) = get_fn( argc );
    got_fn( argc, 1 );

    return 0;
}
""",
        """
import sys

def void myfn( int unused, int i ):
    pass

def function( void, ( int, int ) ) get_fn( int unused ):
    return myfn

function(void, ( int, int ) ) got_fn = get_fn( len( sys.argv ) )
got_fn( len( sys.argv ), 1 )
"""
)



# TODO: remove need for "unused" arguments, by making
# things runtime by default
def Can_render_function_taking_function_as_arg__test():
    assert_rendered_program_equals(
        """
int fn1( double a, double b );
void myfn( int unused, int (*myarg)( double, double ) );

int fn1( double a, double b )
{
    return 1;
}

void myfn( int unused, int (*myarg)( double, double ) )
{
}

int main( int argc, char* argv[] )
{
    myfn( argc, fn1 );

    return 0;
}
""",
        """
import sys

def int fn1( float a, float b ):
    return 1

def void myfn( int unused, function( int, ( float, float ) ) myarg ):
    pass

myfn( len( sys.argv ), fn1 )
"""
)


def Can_render_function_passed_as_arg__test():
    assert_rendered_program_equals(
        """
int fn1( int unused, double n );
void myfn( int unused, int (*myarg)( int, double ) );

int fn1( int unused, double n )
{
    return 1;
}

void myfn( int unused, int (*myarg)( int, double ) )
{
    myarg( unused, 2.0 );
}

int main( int argc, char* argv[] )
{
    myfn( argc, fn1 );

    return 0;
}
""",
        """
import sys

def int fn1( int unused, float n ):
    return 1

def void myfn( int unused, function( int, ( int, float ) ) myarg ):
    myarg( unused, 2.0 )

myfn( len( sys.argv ), fn1 )
"""
)



def Can_render_function_passed_as_arg_taking_class__test():
    assert_rendered_program_equals(
        """
struct Cls
{
};

void Cls_pep_c_pep___init__( Cls& self, int unused );
int fn1( int unused, Cls& c );
void myfn( int unused, int (*myarg)( int, Cls& ) );

void Cls_pep_c_pep___init__( Cls& self, int unused )
{
}

int fn1( int unused, Cls& c )
{
    return 1;
}

void myfn( int unused, int (*myarg)( int, Cls& ) )
{
    myarg( unused, 2.0 );
}

int main( int argc, char* argv[] )
{
    Cls x; Cls_pep_c_pep___init__( x, argc );
    fn1( argc, x );
    myfn( argc, fn1 );

    return 0;
}
""",
        """
import sys

class Cls:
    def_init( Cls self, int unused ):
        pass

def int fn1( int unused, Cls c ):
    return 1

def void myfn( int unused, function( int, ( int, Cls ) ) myarg ):
    myarg( unused, 2.0 )

Cls x = Cls.init( len( sys.argv ) )
fn1( len( sys.argv ), x )
myfn( len( sys.argv ), fn1 )
"""
)


def Now_evaluates_now_but_otherwise_not__test():
    """
        If we render some stuff that could be evaluated at
        compile time, it is not evaluated, unless we wrap it
        in a call to the now() builtin.
    """

    assert_rendered_program_equals(
        r"""#include <stdio.h>

int main( int argc, char* argv[] )
{
    printf( "%d\n", (3 * 2) );
    printf( "%d\n", 6 );

    return 0;
}
""",
        """
print( 3 * 2 )
print( now( 3 *2 ) )
"""
)




