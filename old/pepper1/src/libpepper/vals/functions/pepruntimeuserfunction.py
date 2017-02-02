# Copyright (C) 2011-2013 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

# My days are swifter than a runner; they fly away without a glimpse
# of joy. Job 9 v25

from libpepper.values import PepValue

class PepRuntimeUserFunction( PepValue ):
    def __init__( self, user_function, args, namespace_name ):
        PepValue.__init__( self )
        # TODO: check arg types
        self.user_function = user_function
        self.args = args
        self.namespace_name = namespace_name

    def construction_args( self ):
        return ( self.user_function, self.args, self.namespace_name )

    def is_known( self, env ):
        return False

    def evaluated_type( self, env ):
        return self.user_function.return_type( self.args, env )

