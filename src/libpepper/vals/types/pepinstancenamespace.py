# Copyright (C) 2012-2013 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

# Let love and faithfulness never leave you; bind them round your neck, write
# them on the tablet of your heart.  Proverbs 3 v3

from libpepper.namespace import PepNamespace
from libpepper.vals.functions import PepFunctionOverloadList

from pepinstancemethod import PepInstanceMethod

class PepInstanceNamespace( PepNamespace ):
    """
    The namespace of an instance of a class.
    When an instance is asked for one of its methods, it will return a bound
    method (a PepInstanceMethod).  The way it does that is by having an
    instance of this class as its namespace instead of a normal namespace.
    When we look up a name in this namespace and find a function, we bind
    it to the instance before we return it.
    """

    def __init__( self, instance, class_namespace ):
        #type_implements( PepInstance, instance )
        #type_implements( dict,        class_namespace )
        PepNamespace.__init__( self )
        self.instance = instance
        self.class_namespace = class_namespace

    def _find( self, key ):

        found = PepNamespace._find( self, key )
        if found is not None:
            return found

        found = self.class_namespace._find( key )
        if isinstance( found, PepFunctionOverloadList ):
            return PepFunctionOverloadList(
                map(
                    lambda fn: PepInstanceMethod( self.instance, fn ),
                    found._list
                )
            )
        else:
            return found

