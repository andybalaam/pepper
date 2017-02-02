# Copyright (C) 2013 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

# Bear with me while I speak,
#     and after I have spoken, mock on.
# Job 21 v3

from nose.tools import *

from test.asserts import eval_statement

from libpepper import builtins
from libpepper.environment import PepEnvironment
from libpepper.cpp.cpprenderer import PepCppRenderer

from libpepper.vals.all_values import *

def Function_type_evaluates_to_PepFunctionType__test():

    env = PepEnvironment( PepCppRenderer() )
    builtins.add_builtins( env )

    ans = eval_statement( env, "function( float, ( string, int ) )" )

    assert_equal( PepFunctionType, ans.__class__ )
    assert_equal( PepType( PepFloat ), ans.return_type )
    assert_equal( PepTuple, ans.arg_types.__class__ )
    assert_equal( PepType( PepString ), ans.arg_types.items[0] )
    assert_equal( PepType( PepInt ),    ans.arg_types.items[1] )


