# Copyright (C) 2014 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

from libpepper.values import PepValue

class PepCodeBlock( PepValue ):
    def __init__( self, arg_types_and_names, body_stmts ):
        self.arg_types_and_names = arg_types_and_names
        self.body_stmts = body_stmts

    def construction_args( self ):
        return ( self.arg_types_and_names, self.body_stmts )

