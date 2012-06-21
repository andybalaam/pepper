
from nose.tools import *

from libeeyore.builtins import add_builtins
from libeeyore.classvalues import *
from libeeyore.environment import EeyEnvironment
from libeeyore.cpp.cppvalues import *
from libeeyore.cpp.cpprenderer import EeyCppRenderer

from libeeyore.usererrorexception import EeyUserErrorException

from eeyasserts import assert_contains
from eeyasserts import assert_multiline_equal

def test_Static_variable_can_be_read():
    env = EeyEnvironment( EeyCppRenderer() )

    decl = EeyClass(
        name=EeySymbol( "MyClass" ),
        base_classes=(),
        body_stmts=(
            EeyInit( EeyType( EeyInt ), EeySymbol( "i" ), EeyInt( "7" ) ),
        )
    )

    assert_equal( decl.render( env ), "" )

    value = EeySymbol( "MyClass.i" )

    assert_equal( value.render( env ), "7" )


def test_Member_function_can_be_executed():
    """
    Note this test may turn out to be incorrect.  Python would respond with:
        TypeError: unbound method myfunc() must be called with X instance as
        first argument (got int instance instead)
    """

    env = EeyEnvironment( EeyCppRenderer() )

    decl = EeyClass(
        name=EeySymbol( "MyClass" ),
        base_classes=(),
        body_stmts=(
            EeyDef(
                EeyType( EeyInt ),
                EeySymbol( "myfunc" ),
                (
                    ( EeyType( EeyInt ), EeySymbol( "x" ) ),
                ),
                (
                    EeyReturn( EeySymbol( "x" ) ),
                )
            ),
        )
    )

    assert_equal( decl.render( env ), "" )

    value3 = EeyFunctionCall(
        EeySymbol( "MyClass.myfunc" ),
        (
            EeyInt( "3" ),
        )
    )

    value5 = EeyFunctionCall(
        EeySymbol( "MyClass.myfunc" ),
        (
            EeyInt( "5" ),
        )
    )

    assert_equal( value5.render( env ), "5" )


def test_Init_returns_a_new_instance():

    env = EeyEnvironment( EeyCppRenderer() )

    decl = EeyClass(
        name=EeySymbol( "MyClass" ),
        base_classes=(),
        body_stmts=(
            EeyPass(),
        )
    )

    assert_equal( decl.render( env ), "" )

    value = EeyFunctionCall( EeySymbol( "MyClass.init" ), () )
    ev_value = value.evaluate( env )

    assert_equal( ev_value.__class__, EeyInstance )
    assert_equal( ev_value.get_class_name(), "MyClass" )


def test_Init_with_arg_returns_new_instance_constructed_with_arg():
    env = EeyEnvironment( EeyCppRenderer() )
    add_builtins( env )

    decl = EeyClass(
        name=EeySymbol( "MyClass" ),
        base_classes=(),
        body_stmts=(
            EeyDefInit(
                (
                    ( EeySymbol( "MyClass" ), EeySymbol( 'self' ) ),
                    ( EeySymbol( "int" ), EeySymbol( 'a' ) ),
                ),
                (
                    (
                        EeyVar(
                            (
                                EeyInit(
                                    EeySymbol( "int" ),
                                    EeySymbol( "self.x" ),
                                    EeySymbol( "a" )
                                ),
                            )
                        ),
                    )
                ),
            ),
        )
    )

    assert_equal( "", decl.render( env ) )

    make_instance = EeyInit(
        EeySymbol( "MyClass" ),
        EeySymbol( "my_instance" ),
        EeyFunctionCall(
            EeySymbol( "MyClass.init" ), ( EeyInt( "3" ), )
        )
    )

    assert_equal( "", make_instance.render( env ) )

    value = EeySymbol( "my_instance.x" )

    assert_equal( "3", value.render( env ) )


def test_Can_get_names_of_member_variables_from_def_init():

    env = EeyEnvironment( EeyCppRenderer() )
    add_builtins( env )

    definit = EeyDefInit(
        ( ( EeySymbol( "MyClass" ), EeySymbol( 'fooself' ) ), ),
        (
            (
                EeyVar(
                    (
                        EeyInit(
                            EeySymbol( "int" ),
                            EeySymbol( "fooself.member_one" ),
                            EeyInt( 0 )
                        ),
                        EeyInit(
                            EeySymbol( "float" ),
                            EeySymbol( "fooself.member_two" ),
                            EeyFloat( 0.1 )
                        ),
                    )
                ),
            )
        ),
    ).evaluate( env )

    assert_equal(
        str( [
            ( EeySymbol( "int" ),   "member_one" ),
            ( EeySymbol( "float" ), "member_two" )
        ] ),
        str( definit.get_member_variables() )
    )


def test_Not_allowed_non_self_inits_in_var():

    env = EeyEnvironment( EeyCppRenderer() )
    add_builtins( env )

    definit = EeyDefInit(
        ( ( EeySymbol( "MyClass" ), EeySymbol( 'barself' ) ), ),
        (
            (
                EeyVar(
                    (
                        EeyInit(
                            EeySymbol( "int" ),
                            EeySymbol( "my_var" ),
                            EeyInt( 0 )
                        ),
                    )
                ),
            )
        ),
    )

    exception_caught = False
    try:
        definit.get_member_variables()
    except EeyUserErrorException, e:
        exception_caught = True
        assert_contains( str( e ), "'my_var' does not start with 'barself.'" )

    assert( exception_caught )


def test_Must_provide_nonempty_variable_name_in_var():

    env = EeyEnvironment( EeyCppRenderer() )
    add_builtins( env )

    definit = EeyDefInit(
        ( ( EeySymbol( "MyClass" ), EeySymbol( 'self' ) ), ),
        (
            (
                EeyVar(
                    (
                        EeyInit(
                            EeySymbol( "int" ),
                            EeySymbol( "self." ),
                            EeyInt( 0 )
                        ),
                    )
                ),
            )
        ),
    )

    exception_caught = False
    try:
        definit.get_member_variables()
    except EeyUserErrorException, e:
        exception_caught = True
        assert_contains(
            str( e ),
            "You must provide a variable name, not just 'self.'"
        )

    assert( exception_caught )



def test_Can_get_names_of_member_variables_from_class():

    env = EeyEnvironment( EeyCppRenderer() )
    add_builtins( env )

    cls = EeyUserClass(
        name="MyClass",
        base_classes=(),
        body_stmts=(
            EeyDefInit(
                ( ( EeySymbol( "MyClass" ), EeySymbol( 'self' ) ), ),
                (
                    (
                        EeyVar(
                            (
                                EeyInit(
                                    EeySymbol( "int" ),
                                    EeySymbol( "self.member_one" ),
                                    EeyInt( 0 )
                                ),
                                EeyInit(
                                    EeySymbol( "float" ),
                                    EeySymbol( "self.member_two" ),
                                    EeyFloat( 0.1 )
                                ),
                            )
                        ),
                    )
                ),
            ),
        )
    ).evaluate( env )

    assert_equal(
        str( [
            ( EeySymbol( "int" ),   "member_one" ),
            ( EeySymbol( "float" ), "member_two" )
        ] ),
        str( cls.member_variables )
    )



def test_Class_reports_methods_available():

    env = EeyEnvironment( EeyCppRenderer() )
    add_builtins( env )

    cls = EeyUserClass(
        name="MyClass",
        base_classes=(),
        body_stmts=(
            EeyDef(
                EeyType( EeyInt ),
                EeySymbol( "myfunc" ),
                (
                    ( EeySymbol( "MyClass" ), EeySymbol( "self" ) ),
                ),
                (
                    EeyReturn( EeyInt( "3" ) ),
                )
            ),
        )
    ).evaluate( env )

    assert_true( "myfunc"  in cls.get_namespace() )
    assert_true( "foo" not in cls.get_namespace() )


def test_Class_reports_properties_available():

    env = EeyEnvironment( EeyCppRenderer() )
    add_builtins( env )

    cls = EeyUserClass(
        name="MyClass",
        base_classes=(),
        body_stmts=(
            EeyDefInit(
                ( ( EeySymbol( "MyClass" ), EeySymbol( 'self' ) ), ),
                (
                    (
                        EeyVar(
                            (
                                EeyInit(
                                    EeySymbol( "int" ),
                                    EeySymbol( "self.myprop" ),
                                    EeyInt( 0 )
                                ),
                            )
                        ),
                    )
                ),
            ),
        )
    ).evaluate( env )

    assert_true( "myprop"  in cls.get_namespace() )
    assert_true( "foo" not in cls.get_namespace() )


