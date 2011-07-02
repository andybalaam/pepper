
from itertools import imap

from buildstep import BuildStep
from parse import EeyoreParser
from parse import EeyoreTreeWalker

def _parse_tree_string_to_values( string ):
    from functionvalues import *
    from languagevalues import *
    from values import *

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
            filter( non_empty_line,
                imap( remove_comments, parse_tree_in_fl ) ) )

    def process( self, val ):
        parser = EeyoreParser.Parser( val )
        parser.program()
        walker = EeyoreTreeWalker.Walker()
        return [walker.functionCall( parser.getAST() )]

    def write_to_file( self, val, fl ):
        raise Exception( "TODO" )

