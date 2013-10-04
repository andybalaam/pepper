# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

# As for everyone who comes to me and hears my words and puts them into
# practice, I will show you what they are like.  Luke 6 v47

from libpepper.all_known import all_known
from libpepper.values import PepTypeMatcher
from libpepper.values import PepValue

class PepFunctionType( PepValue, PepTypeMatcher ):
    def __init__( self, return_type, arg_types ):
        PepValue.__init__( self )
        self.return_type = return_type
        self.arg_types = arg_types

    def construction_args( self ):
        return ( self.return_type, self.arg_types )

    def do_evaluate( self, env ):
        return PepFunctionType(
            self.return_type.evaluate( env ),
            self.arg_types.evaluate( env ),
        )

    def is_known( self, env ):
        return all_known( ( self.return_type, self.arg_types ), env )

    def matches( self, other, env ):
        #if ( not isinstance( other, PepCallable ) ):
        #    return False
        # TODO: check type signature
        return True

    def underlying_class( self ):
        return None

    def get_name( self ):
        return None

    def runtime_namespace( self, instance, insert_placeholders ):
        return None

    def get_namespace( self ):
        return None

