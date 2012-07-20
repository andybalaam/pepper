
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



class FakeFn( object ):
    def call( self, env, args ):
        return "FakeFn ret val"

class FakeClass( object ):
    def __init__( self ):
        self.name = "FakeClass"

    def get_namespace( self ):
        return {}

def create_method():
    clazz = FakeClass()
    instance = EeyInstance( clazz )
    fn = FakeFn()
    return EeyInstanceMethod( instance, fn )

def test_Calling_a_method_with_known_args_returns_the_answer():

    # Create a method on an instance, which uses a function we expect
    # to be called
    meth = create_method()

    # This is what we are testing: the underlying function was called
    assert_equal(
        "FakeFn ret val",
        meth.call( "env", ( EeyInt( "3" ), EeyInt( "4" ) ) )
    )

def test_Calling_a_method_with_unknown_args_returns_a_runtime_function():

    # Create a method on an instance
    meth = create_method()

    # This is what we are testing: we returned an EeyRuntimeUserFunction
    # because an argument was unknown
    assert_equal(
        EeyRuntimeUserFunction,
        meth.call(
            "env", ( EeyInt( "3" ), EeyVariable( EeyInt, "x" ) ) ).__class__
    )

def test_Calling_a_method_with_unknown_instance_returns_a_runtime_function():

    # Create a method on a runtime instance
    clazz = FakeClass()
    instance = EeyRuntimeInstance( clazz, "inst" )
    fn = FakeFn()
    meth = EeyInstanceMethod( instance, fn )

    # This is what we are testing: we returned an EeyRuntimeUserFunction
    # because the instance was unknown
    assert_equal(
        EeyRuntimeUserFunction,
        meth.call(
            "env", ( EeyInt( "3" ), EeyInt( "3" ) ) ).__class__
    )


def test_Instances_return_their_own_values_overriding_class_values():
    clazz = FakeClass()
    inst = EeyInstance( clazz )

    # Put values into both the class and the instance (instance first to
    # avoid errors if I decide it is an error to override in a subnamespace)
    inst.get_namespace()["a"] = "return_me"
    clazz.get_namespace()["a"] = "dont_return_me"

    # This is what we are testing: the instance one wins
    assert_equal( "return_me", inst.get_namespace()["a"] )


def test_Instances_return_class_values_where_they_have_nothing():

    class MyClass( object ):
        def __init__( self ):
            self.namespace = EeyNamespace()

        def get_namespace( self ):
            return self.namespace

    clazz = MyClass()
    inst = EeyInstance( clazz )

    # Put a values into the class
    clazz.get_namespace()["a"] = "class_value"

    # This is what we are testing: we find it in the class
    assert_equal( "class_value", inst.get_namespace()["a"] )


def test_Instance_returns_a_method_when_class_holds_a_function():

    class MyClass( object ):
        def __init__( self ):
            self.namespace = EeyNamespace()

        def get_namespace( self ):
            return self.namespace

    clazz = MyClass()
    inst = EeyInstance( clazz )
    fn = "fake_fn"

    # Put values into both the class and the instance
    clazz.get_namespace()["a"] = EeyFunctionOverloadList( [fn] )

    # This is what we are testing: get the function out via the instance
    ans = inst.get_namespace()["a"]

    # The function was wrapped as a method
    ans_fn = ans._list[0]
    assert_equal( EeyInstanceMethod, ans_fn.__class__ )
    assert_equal( inst, ans_fn.instance )
    assert_equal( fn, ans_fn.fn )




