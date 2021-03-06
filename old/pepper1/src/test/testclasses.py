# Copyright (C) 2012-2013 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


from nose.tools import *

from libpepper.builtins import add_builtins
from libpepper.environment import PepEnvironment
from libpepper.cpp.cppvalues import *
from libpepper.cpp.cpprenderer import PepCppRenderer

from libpepper.vals.all_values import *

from libpepper.usererrorexception import PepUserErrorException

from pepasserts import assert_contains
from pepasserts import assert_multiline_equal

def render_evald( val, env ):
    return val.evaluate( env ).render( env )

def test_Static_variable_can_be_read():
    env = PepEnvironment( PepCppRenderer() )

    decl = PepClass(
        name=PepSymbol( "MyClass" ),
        base_classes=(),
        body_stmts=(
            PepInit( PepType( PepInt ), PepSymbol( "i" ), PepInt( "7" ) ),
        )
    )

    assert_equal( render_evald( decl, env ), "" )

    value = PepSymbol( "MyClass.i" )

    assert_equal( render_evald( value, env ), "7" )


def test_Member_function_can_be_executed():
    """
    Note this test may turn out to be incorrect.  Python would respond with:
        TypeError: unbound method myfunc() must be called with X instance as
        first argument (got int instance instead)
    """

    env = PepEnvironment( PepCppRenderer() )

    decl = PepClass(
        name=PepSymbol( "MyClass" ),
        base_classes=(),
        body_stmts=(
            PepDef(
                PepType( PepInt ),
                PepSymbol( "myfunc" ),
                (
                    ( PepType( PepInt ), PepSymbol( "x" ) ),
                ),
                (
                    PepReturn( PepSymbol( "x" ) ),
                )
            ),
        )
    )

    assert_equal( render_evald( decl, env ), "" )

    value3 = PepFunctionCall(
        PepSymbol( "MyClass.myfunc" ),
        (
            PepInt( "3" ),
        )
    )

    value5 = PepFunctionCall(
        PepSymbol( "MyClass.myfunc" ),
        (
            PepInt( "5" ),
        )
    )

    assert_equal( render_evald( value5, env ), "5" )


def test_Init_returns_a_new_instance():

    env = PepEnvironment( PepCppRenderer() )

    decl = PepClass(
        name=PepSymbol( "MyClass" ),
        base_classes=(),
        body_stmts=(
            PepPass(),
        )
    )

    assert_equal( render_evald( decl, env ), "" )

    value = PepFunctionCall( PepSymbol( "MyClass.init" ), () )
    ev_value = value.evaluate( env )

    assert_equal( PepKnownInstance, ev_value.__class__ )
    assert_equal( "MyClass", ev_value.clazz.name )


def test_Init_with_arg_returns_new_instance_constructed_with_arg():
    env = PepEnvironment( PepCppRenderer() )
    add_builtins( env )

    decl = PepClass(
        name=PepSymbol( "MyClass" ),
        base_classes=(),
        body_stmts=(
            PepDefInit(
                (
                    ( PepSymbol( "MyClass" ), PepSymbol( 'self' ) ),
                    ( PepSymbol( "int" ), PepSymbol( 'a' ) ),
                ),
                (
                    (
                        PepVar(
                            (
                                PepInit(
                                    PepSymbol( "int" ),
                                    PepSymbol( "self.x" ),
                                    PepSymbol( "a" )
                                ),
                            )
                        ),
                    )
                ),
            ),
        )
    )

    assert_equal( "", render_evald( decl, env ) )

    make_instance = PepInit(
        PepSymbol( "MyClass" ),
        PepSymbol( "my_instance" ),
        PepFunctionCall(
            PepSymbol( "MyClass.init" ), ( PepInt( "3" ), )
        )
    )

    assert_equal( "", render_evald( make_instance, env ) )

    value = PepSymbol( "my_instance.x" )

    assert_equal( "3", render_evald( value, env ) )


def test_Can_get_names_of_member_variables_from_def_init():

    env = PepEnvironment( PepCppRenderer() )
    add_builtins( env )

    definit = PepDefInit(
        ( ( PepSymbol( "MyClass" ), PepSymbol( 'fooself' ) ), ),
        (
            (
                PepVar(
                    (
                        PepInit(
                            PepSymbol( "int" ),
                            PepSymbol( "fooself.member_one" ),
                            PepInt( 0 )
                        ),
                        PepInit(
                            PepSymbol( "float" ),
                            PepSymbol( "fooself.member_two" ),
                            PepFloat( 0.1 )
                        ),
                    )
                ),
            )
        ),
    ).evaluate( env )

    assert_equal(
        str( [
            ( PepSymbol( "int"   ).evaluate( env ), "member_one" ),
            ( PepSymbol( "float" ).evaluate( env ), "member_two" )
        ] ),
        str( definit.get_member_variables( env ) )
    )


def test_Not_allowed_non_self_inits_in_var():

    env = PepEnvironment( PepCppRenderer() )
    add_builtins( env )

    definit = PepDefInit(
        ( ( PepSymbol( "MyClass" ), PepSymbol( 'barself' ) ), ),
        (
            (
                PepVar(
                    (
                        PepInit(
                            PepSymbol( "int" ),
                            PepSymbol( "my_var" ),
                            PepInt( 0 )
                        ),
                    )
                ),
            )
        ),
    )

    exception_caught = False
    try:
        definit.get_member_variables( env )
    except PepUserErrorException, e:
        exception_caught = True
        assert_contains( str( e ), "'my_var' does not start with 'barself.'" )

    assert( exception_caught )


def test_Must_provide_nonempty_variable_name_in_var():

    env = PepEnvironment( PepCppRenderer() )
    add_builtins( env )

    definit = PepDefInit(
        ( ( PepSymbol( "MyClass" ), PepSymbol( 'self' ) ), ),
        (
            (
                PepVar(
                    (
                        PepInit(
                            PepSymbol( "int" ),
                            PepSymbol( "self." ),
                            PepInt( 0 )
                        ),
                    )
                ),
            )
        ),
    )

    exception_caught = False
    try:
        definit.get_member_variables( env )
    except PepUserErrorException, e:
        exception_caught = True
        assert_contains(
            str( e ),
            "You must provide a variable name, not just 'self.'"
        )

    assert( exception_caught )



def Cannot_overwrite_method_with_member_variable__test():

    env = PepEnvironment( PepCppRenderer() )
    add_builtins( env )

    decl = PepClass(
        name=PepSymbol( "MyClass" ),
        base_classes=(),
        body_stmts=(
            PepDefInit(
                (
                    ( PepSymbol( "MyClass" ), PepSymbol( 'self' ) ),
                ),
                (
                    (
                        PepVar(
                            (
                                PepInit(
                                    PepSymbol( "int" ),
                                    PepSymbol( "self.my_meth" ),
                                    PepInt( "3" )
                                ),
                            )
                        ),
                    )
                ),
            ),
            PepDef(
                PepSymbol( "void" ),
                PepSymbol( "my_meth" ),
                (
                    ( PepSymbol( "MyClass" ), PepSymbol( 'self' ) ),
                ),
                (
                    PepPass(),
                ),
            ),
        )
    )

    assert_equal( "", render_evald( decl, env ) )

    exception_caught = False
    try:

        make_instance = PepInit(
            PepSymbol( "MyClass" ),
            PepSymbol( "my_instance" ),
            PepFunctionCall(
                PepSymbol( "MyClass.init" ), ()
            )
        )

        render_evald( make_instance, env )

    except PepUserErrorException, e:
        exception_caught = True
        assert_contains(
            str( e ),
            "Namespace already contains the name 'my_meth'"
        )

    assert( exception_caught )



def test_Can_get_names_of_member_variables_from_class():

    env = PepEnvironment( PepCppRenderer() )
    add_builtins( env )

    cls = PepUserClass(
        name="MyClass",
        base_classes=(),
        body_stmts=(
            PepDefInit(
                ( ( PepSymbol( "MyClass" ), PepSymbol( 'self' ) ), ),
                (
                    (
                        PepVar(
                            (
                                PepInit(
                                    PepSymbol( "int" ),
                                    PepSymbol( "self.member_one" ),
                                    PepInt( 0 )
                                ),
                                PepInit(
                                    PepSymbol( "float" ),
                                    PepSymbol( "self.member_two" ),
                                    PepFloat( 0.1 )
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
            ( PepSymbol( "int"   ).evaluate( env ), "member_one" ),
            ( PepSymbol( "float" ).evaluate( env ), "member_two" )
        ] ),
        str( cls.member_variables )
    )



def test_Class_reports_methods_available():

    env = PepEnvironment( PepCppRenderer() )
    add_builtins( env )

    cls = PepUserClass(
        name="MyClass",
        base_classes=(),
        body_stmts=(
            PepDef(
                PepType( PepInt ),
                PepSymbol( "myfunc" ),
                (
                    ( PepSymbol( "MyClass" ), PepSymbol( "self" ) ),
                ),
                (
                    PepReturn( PepInt( "3" ) ),
                )
            ),
        )
    ).evaluate( env )

    assert_true( "myfunc"  in cls.get_namespace() )
    assert_true( "foo" not in cls.get_namespace() )




class FakeFn( object ):
    def call( self, args, env ):
        return "FakeFn ret val"

class FakeClass( object ):
    def __init__( self ):
        self.name = "FakeClass"

    def get_namespace( self ):
        return {}

    def get_name( self ):
        return self.name

def create_method():
    clazz = FakeClass()
    instance = PepKnownInstance( clazz )
    fn = FakeFn()
    return PepInstanceMethod( instance, fn )

def test_Calling_a_method_with_known_args_returns_the_answer():

    # Create a method on an instance, which uses a function we expect
    # to be called
    meth = create_method()

    # This is what we are testing: the underlying function was called
    assert_equal(
        "FakeFn ret val",
        meth.call( ( PepInt( "3" ), PepInt( "4" ) ), "env" )
    )

def test_Calling_a_method_with_unknown_args_returns_a_runtime_function():

    # Create a method on an instance
    meth = create_method()

    # This is what we are testing: we returned an PepRuntimeUserFunction
    # because an argument was unknown
    assert_equal(
        PepRuntimeUserFunction,
        meth.call(
            (
                PepInt( "3" ),
                PepVariable( PepType( PepInt ), "x" ) ),
                "env"
            ).__class__
    )

def test_Calling_a_method_with_unknown_instance_returns_a_runtime_function():

    class FakeType( PepTypeMatcher ):
        def __init__( self ):
            self.name = ""
        def get_name( self ): pass
        def runtime_namespace( self, instance, insert_placeholders ):
            pass
        def get_namespace(): pass
        def matches(): pass
        def underlying_class(): pass

    # Create a method on a variable holding a class type
    clazz = FakeType()
    instance = PepVariable( clazz, "inst" )
    fn = FakeFn()
    meth = PepInstanceMethod( instance, fn )

    # This is what we are testing: we returned an PepRuntimeUserFunction
    # because the instance was unknown
    assert_equal(
        PepRuntimeUserFunction,
        meth.call(
            ( PepInt( "3" ), PepInt( "3" ) ), "env" ).__class__
    )


class MyInstance( PepInstance ):
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
            self.namespace = PepNamespace()

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
            self.namespace = PepNamespace()

        def get_namespace( self ):
            return self.namespace

    clazz = MyClass()
    inst = MyInstance( clazz )
    fn = "fake_fn"

    # Put values into both the class and the instance
    clazz.get_namespace()["a"] = PepFunctionOverloadList( [fn] )

    # This is what we are testing: get the function out via the instance
    ans = inst.get_namespace()["a"]

    # The function was wrapped as a method
    ans_fn = ans._list[0]
    assert_equal( PepInstanceMethod, ans_fn.__class__ )
    assert_equal( inst, ans_fn.instance )
    assert_equal( fn, ans_fn.fn )


def create_instance_variable_and_method_call( env ):
    env.namespace['a'] = PepVariable( PepType( PepInt ), "a" )

    PepClass(
        PepSymbol( 'MyClass' ),
        (),
        (
            PepDefInit(
                (
                    ( PepSymbol('MyClass'), PepSymbol('self') ),
                    ( PepType( PepInt ), PepSymbol('x') ),
                ),
                ( PepPass(), )
            ),
            PepDef(
                PepType( PepVoid ),
                PepSymbol('my_meth'),
                ( ( PepSymbol('MyClass'), PepSymbol('self') ), ),
                ( PepPass(), )
            )
        )
    ).evaluate( env )

    PepInit(
        PepSymbol( 'MyClass' ),
        PepSymbol( 'mc' ),
        PepFunctionCall( PepSymbol( 'MyClass.init' ), ( PepSymbol( "a" ), ) )
    ).evaluate( env )

    meth = PepFunctionCall( PepSymbol( "mc.my_meth" ), () )

    return meth

def Runtime_instance_has_evaluated_type_of_class___test():
    env = PepEnvironment( None )
    meth = create_instance_variable_and_method_call( env )

    assert_equal(
        PepSymbol( "MyClass" ).evaluate( env ),
        PepSymbol( "mc" ).evaluated_type( env )
    )


def Runtime_instance_allows_access_to_methods___test():
    env = PepEnvironment( None )
    meth = create_instance_variable_and_method_call( env )

    # my_meth is a callable taking no args and returning void
    assert_equal(
        PepType( PepVoid ),
        PepSymbol( "mc.my_meth" ).evaluate( env ).return_type( (), env )
    )

    # The methods are not known since the instance isn't
    assert_false( PepSymbol( "mc.my_meth" ).evaluate( env ).is_known( env ) )



def Method_calls_of_instance_variables_are_unknown___test():
    env = PepEnvironment( None )
    meth = create_instance_variable_and_method_call( env )

    assert_false( meth.is_known( env ) )

    ev_meth = meth.evaluate( env )

    assert_false( ev_meth.is_known( env ) )


def Evaluated_types_of_method_calls_of_instance_variables_are_correct___test():
    env = PepEnvironment( None )
    meth = create_instance_variable_and_method_call( env )

    assert_equal( PepType( PepVoid ), meth.evaluated_type( env ) )

    ev_meth = meth.evaluate( env )

    assert_equal( PepType( PepVoid ), ev_meth.evaluated_type( env ) )

@raises(PepUserErrorException)
def No_method_called_init_allowed__test():
    env = PepEnvironment( None )
    PepUserClass(
        name=PepSymbol( "MyClass" ),
        base_classes=(),
        body_stmts=(
            PepDef( PepType( PepInt ), PepSymbol( "init" ), (), (PepPass(),) ),
        )
    ).evaluate( env )

@raises(PepUserErrorException)
def No_method_called_implements_allowed__test():
    env = PepEnvironment( None )
    PepUserClass(
        name=PepSymbol( "MyClass" ),
        base_classes=(),
        body_stmts=(
            PepDef(
                PepType( PepInt ),
                PepSymbol( "implements" ),
                (),
                (PepPass(),)
            ),
        )
    ).evaluate( env )

def Builtin_implements_method_does_not_break_implements_check__test():
    # At one point checking for an "implements" method was actually failing
    # because a global "implements" function existed - this test fails if
    # that happens.

    env = PepEnvironment( None )
    add_builtins( env )
    PepUserClass(
        name=PepSymbol( "MyClass" ),
        base_classes=(),
        body_stmts=(
            PepPass(),
        )
    ).evaluate( env )

