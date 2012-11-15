# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


from nose.tools import *

from libpepper.environment import PepEnvironment
from libpepper.vals.all_values import *

env = PepEnvironment( None )

def test_Int_matches_Int():
    the_type = PepType( PepInt )
    the_value = PepInt( "3" )
    assert_true( the_type.matches( the_value.evaluated_type( env ) ) )

def test_Float_doesnt_match_Int():
    the_type = PepType( PepFloat )
    the_value = PepInt( "3" )
    assert_false( the_type.matches( the_value.evaluated_type( env ) ) )

def test_Int_doesnt_match_class_instance():
    the_type = PepType( PepFloat )
    the_value = PepUserClass( "MyClass", (), (PepPass(),) ).known_instance()
    assert_false( the_type.matches( the_value.evaluated_type( env ) ) )

def test_Class_matches_instance():
    the_type = PepUserClass( "MyClass", (), (PepPass(),) )
    the_value = the_type.known_instance()
    assert_true( the_type.matches( the_value.evaluated_type( env ) ) )

def test_Class_doesnt_match_instance_of_other():
    the_type = PepUserClass( "MyClass", (), (PepPass(),) )
    the_other_type = PepUserClass( "MyOtherClass", (), (PepPass(),) )
    the_value = the_other_type.known_instance()
    assert_false( the_type.matches( the_value.evaluated_type( env ) ) )

def test_Class_doesnt_match_Int():
    the_type = PepUserClass( "MyClass", (), (PepPass(),) )
    the_value = PepInt( "34" )
    assert_false( the_type.matches( the_value.evaluated_type( env ) ) )


