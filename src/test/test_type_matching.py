
from nose.tools import *

from libeeyore.environment import EeyEnvironment
from libeeyore.values import *
from libeeyore.classvalues import *

env = EeyEnvironment( None )

def test_Int_matches_Int():
    the_type = EeyType( EeyInt )
    the_value = EeyInt( "3" )
    assert_true( the_type.matches( the_value.evaluated_type( env ) ) )

def test_Float_doesnt_match_Int():
    the_type = EeyType( EeyFloat )
    the_value = EeyInt( "3" )
    assert_false( the_type.matches( the_value.evaluated_type( env ) ) )

def test_Int_doesnt_match_class_instance():
    the_type = EeyType( EeyFloat )
    the_value = EeyUserClass( "MyClass", (), (EeyPass(),) ).create_instance()
    assert_false( the_type.matches( the_value.evaluated_type( env ) ) )

def test_Class_matches_instance():
    the_type = EeyUserClass( "MyClass", (), (EeyPass(),) )
    the_value = the_type.create_instance()
    assert_true( the_type.matches( the_value.evaluated_type( env ) ) )

def test_Class_doesnt_match_instance_of_other():
    the_type = EeyUserClass( "MyClass", (), (EeyPass(),) )
    the_other_type = EeyUserClass( "MyOtherClass", (), (EeyPass(),) )
    the_value = the_other_type.create_instance()
    assert_false( the_type.matches( the_value.evaluated_type( env ) ) )

def test_Class_doesnt_match_Int():
    the_type = EeyUserClass( "MyClass", (), (EeyPass(),) )
    the_value = EeyInt( "34" )
    assert_false( the_type.matches( the_value.evaluated_type( env ) ) )


