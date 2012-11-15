# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


from itertools import imap

from buildstep import BuildStep

from parse.eeyorestatements import EeyoreStatements

# We would like to do these imports inside _parse_tree_string_to_values,
# but Python doesn't like us to do that.
from libeeyore.functionvalues import *
from libeeyore.languagevalues import *
from libeeyore.values import *

def _parse_tree_string_to_values( string ):
    # The parse tree is actually a valid Python file
    return eval( string )



def _remove_comments( ln ):
    i = ln.find( "#" )
    if i != -1:
        return ln[:i]
    else:
        return ln

def _non_empty_line( ln ):
    return ( ln.strip() != "" )

class ParseBuildStep( BuildStep ):
    def read_from_file( self, fl ):
        return ( _parse_tree_string_to_values( ln ) for ln in
            filter( _non_empty_line,
                imap( _remove_comments, fl ) ) )

    def process( self, val ):
        return EeyoreStatements( val )

    def write_to_file( self, val, fl ):
        for v in val:
            fl.write( repr( v ) )
            fl.write( "\n" )

