# Copyright (C) 2011-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


from libpepper.values import EeyString
from libpepper.values import EeyValue


class EeySysArgv( EeyValue ):

    def __init__( self ):
        EeyValue.__init__( self )

    def construction_args( self ):
        return ()

    def is_known( self, env ):
        False

    def lookup( self, env ):
        return self


class EeySys( EeyValue ):
    def __init__( self ):
        EeyValue.__init__( self )

        self.namespace = {
            "argv"     : EeySysArgv(),
            "copyright": EeyString(
                "Copyright (C) 2010-2012 Andy Balaam and the Pepper developers"
            ),
        }

    def construction_args( self ):
        return ()

    def get_namespace( self ):
        return self.namespace


