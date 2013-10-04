# Copyright (C) 2013 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

# Is there anything of which one can say, 'Look! This is something new'?
# It was here already, long ago; it was here before our time.
# Ecclesiastes 1 v10

from libpepper.values import PepTypeMatcher
from libpepper.values import PepValue

class PepInterfaceTypeMatcher( PepValue, PepTypeMatcher ):
    """
    The result of evaluating implements(MyInterface).  An instance of this
    class is a TypeMatcher that matches against the interface supplied in
    the constructor.
    """
    def __init__( self, interface ):
        self.interface = interface

    def construction_args( self ):
        return ( (self.interface,), )

    def do_evaluate( self, env ):
        return self

    def is_known( self, env ):
        # TODO: support unknown
        return True

    def matches( self, value_type, env ):
        # TODO: check arg is an interface
        return self.interface.can_match( value_type )

    def underlying_class( self ):
        return self.interface

    def get_name( self ):
        self.interface.get_name()

    def runtime_namespace( self, instance, insert_placeholders ):
        return self.get_namespace()

    def get_namespace( self ):
        return self.interface.get_namespace()


