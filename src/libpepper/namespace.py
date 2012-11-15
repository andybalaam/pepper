# Copyright (C) 2011-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


class EeyNamespace( object ):

    def __init__( self, shallower_ns = None ):
        self.shallower_ns = shallower_ns
        self.thedict = {}

    def __contains__( self, key ):
        return ( self._find( key ) is not None )

    def __getitem__( self, key ):
        f = self._find( key )
        if f is None:
            raise KeyError( key )
        return f

    def __setitem__( self, key, value ):
        assert( key not in self.thedict ) # TODO - not an assert
        self.thedict[key] = value

    def overwrite( self, key, value ):
        self.thedict[key] = value

    def _find( self, key ):
        if key in self.thedict:
            return self.thedict[key]
        elif self.shallower_ns is not None:
            return self.shallower_ns._find( key )
        else:
            return None

    def key_for_value( self, value ):
        for k, v in self.thedict.iteritems():
            if value == v:
                return k
        return None

    def iteritems( self ):
        return self.thedict.iteritems()

