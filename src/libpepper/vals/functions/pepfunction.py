# Copyright (C) 2011-2013 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

# For just as each of us has one body with many members, and these members
# do not all have the same function, Romans 12 v4

from libpepper.values import PepValue
from pepcallable import PepCallable

class PepFunction( PepCallable ):

    def __init__( self ):
        PepValue.__init__( self )
#        self.arg_types_and_names = arg_types_and_names

    def is_known( self, env ):
        return True

