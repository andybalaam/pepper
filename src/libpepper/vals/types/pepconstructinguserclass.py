# Copyright (C) 2012-2013 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

# I will make you very fruitful; I will make nations of you, and kings will
# come from you. Genesis 17 v6

from libpepper.languagevalues import PepUninitedMemberVariable
from libpepper.utils.type_is import type_is
from libpepper.values import PepTypeMatcher
from libpepper.values import PepValue

from pepinstancenamespace import PepInstanceNamespace

class PepConstructingUserClass( PepValue, PepTypeMatcher ):
    """
    A wrapper around a class that specifies that it is still
    being constructed.  At the moment this wrapper is automatically
    applied (in cpprenderer.py!) but I think at some point you
    will have to declare it explicitly with something like:
    def_init( constructing(MyClass) self )
    """

    def __init__( self, userclass ):
        PepValue.__init__( self )
        self.userclass = userclass

    def construction_args( self ):
        return ( self.userclass, )

    def matches( self, other ):
        return self.userclass.matches( other )

    def get_name( self ):
        return self.userclass.get_name()

    def underlying_class( self ):
        return self.userclass.underlying_class()

    def get_namespace( self ):
        return self.userclass.get_namespace()

    def runtime_namespace( self, instance, insert_placeholders ):
        #type_implements( PepInstance, instance )
        type_is( bool, insert_placeholders )
        ret = PepInstanceNamespace( instance, self.get_namespace() )
        for var_type, var_name in self.userclass.member_variables:
            ret[var_name] = PepUninitedMemberVariable( var_type, "" )
        return ret

