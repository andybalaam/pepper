# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


from nose.tools import *

from libpepper.builtins import add_builtins
from libpepper.classvalues import *
from libpepper.environment import EeyEnvironment
from libpepper.cpp.cppvalues import *
from libpepper.cpp.cpprenderer import EeyCppRenderer

from libpepper.usererrorexception import EeyUserErrorException

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

    assert_equal( EeyKnownInstance, ev_value.__class__ )
    assert_equal( "MyClass", ev_value.clazz.name )


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
    def call( self, args, env ):
        return "FakeFn ret val"

class FakeClass( object ):
    def __init__( self ):
        self.name = "FakeClass"

    def get_namespace( self ):
        return {}

def create_method():
    clazz = FakeClass()
    instance = EeyKnownInstance( clazz )
    fn = FakeFn()
    return EeyInstanceMethod( instance, fn )

def test_Calling_a_method_with_known_args_returns_the_answer():

    # Create a method on an instance, which uses a function we expect
    # to be called
    meth = create_method()

    # This is what we are testing: the underlying function was called
    assert_equal(
        "FakeFn ret val",
        meth.call( ( EeyInt( "3" ), EeyInt( "4" ) ), "env" )
    )

def test_Calling_a_method_with_unknown_args_returns_a_runtime_function():

    # Create a method on an instance
    meth = create_method()

    # This is what we are testing: we returned an EeyRuntimeUserFunction
    # because an argument was unknown
    assert_equal(
        EeyRuntimeUserFunction,
        meth.call(
            ( EeyInt( "3" ), EeyVariable( EeyInt, "x" ) ), "env" ).__class__
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
            ( EeyInt( "3" ), EeyInt( "3" ) ), "env" ).__class__
    )


class MyInstance( EeyInstance ):
    def construction_args( self ):
        pass

def test_Instances_return_their_own_values_overriding_class_values():
    clazz = FakeClass()
    inst = MyInstance( clazz )

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
    inst = MyInstance( clazz )

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
    inst = MyInstance( clazz )
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


def create_runtime_instance_and_method_call( env ):
    env.namespace['a'] = EeyVariable( EeyType( EeyInt ), "a" )

    EeyClass(
        EeySymbol( 'MyClass' ),
        (),
        (
            EeyDefInit(
                (
                    ( EeySymbol('MyClass'), EeySymbol('self') ),
                    ( EeyType( EeyInt ), EeySymbol('x') ),
                ),
                ( EeyPass(), )
            ),
            EeyDef(
                EeyType( EeyVoid ),
                EeySymbol('my_meth'),
                ( ( EeySymbol('MyClass'), EeySymbol('self') ), ),
                ( EeyPass(), )
            )
        )
    ).evaluate( env )

    EeyInit(
        EeySymbol( 'MyClass' ),
        EeySymbol( 'mc' ),
        EeyFunctionCall( EeySymbol( 'MyClass.init' ), ( EeySymbol( "a" ), ) )
    ).evaluate( env )

    meth = EeyFunctionCall( EeySymbol( "mc.my_meth" ), () )

    return meth

def Runtime_instance_has_evaluated_type_of_class___test():
    env = EeyEnvironment( None )
    meth = create_runtime_instance_and_method_call( env )

    assert_equal(
        EeySymbol( "MyClass" ).evaluate( env ),
        EeySymbol( "mc" ).evaluated_type( env )
    )


def Runtime_instance_allows_access_to_methods___test():
    env = EeyEnvironment( None )
    meth = create_runtime_instance_and_method_call( env )

    # my_meth is a callable taking no args and returning void
    assert_equal(
        EeyType( EeyVoid ),
        EeySymbol( "mc.my_meth" ).evaluate( env ).return_type( (), env )
    )

    # The methods are not known since the instance isn't
    assert_false( EeySymbol( "mc.my_meth" ).evaluate( env ).is_known( env ) )



def Method_calls_of_runtime_instances_are_unknown___test():
    env = EeyEnvironment( None )
    meth = create_runtime_instance_and_method_call( env )

    assert_false( meth.is_known( env ) )

    ev_meth = meth.evaluate( env )

    assert_false( ev_meth.is_known( env ) )


def Evaluated_types_of_method_calls_of_runtime_instances_are_correct___test():
    env = EeyEnvironment( None )
    meth = create_runtime_instance_and_method_call( env )

    assert_equal( EeyType( EeyVoid ), meth.evaluated_type( env ) )

    ev_meth = meth.evaluate( env )

    assert_equal( EeyType( EeyVoid ), ev_meth.evaluated_type( env ) )


