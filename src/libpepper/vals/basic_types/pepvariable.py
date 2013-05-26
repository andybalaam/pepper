# Copyright (C) 2011-2013 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

# He reveals deep and hidden things; he knows what lies in darkness, and
# light dwells with him. Daniel 2 v22

from libpepper.utils.type_is import type_is
from libpepper.utils.type_isinstance import type_isinstance
from libpepper.values import PepTypeMatcher
from libpepper.values import PepValue

class PepVariable( PepValue ):
    def __init__( self, clazz, name ):
        type_isinstance( PepTypeMatcher, clazz )
        type_is(         str,            name )

        PepValue.__init__( self )
        self.clazz = clazz
        self.name = name
        self.namespace = self.clazz.runtime_namespace( self, False )

    def construction_args( self ):
        return ( self.clazz, self.name )

    def is_known( self, env ):
        return False

    def evaluated_type( self, env ):
        return self.clazz.evaluate( env )

    def get_namespace( self ):
        return self.namespace

