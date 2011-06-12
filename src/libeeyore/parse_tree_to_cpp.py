from itertools import imap

import builtins

from cpp.cpprenderer import EeyCppRenderer
from environment import EeyEnvironment
from functionvalues import *
from languagevalues import *
from values import *

def parse_tree_string_to_values( string ):
	return eval( string )

def remove_comments( ln ):
	i = ln.find( "#" )
	if i != -1:
		return ln[:i]
	else:
		return ln

def non_empty_line( ln ):
	return ( ln.strip() != "" )

def parse_tree_to_cpp( parse_tree_in_fl, cpp_out_fl ):
	env = EeyEnvironment( EeyCppRenderer() )
	builtins.add_builtins( env )

	values = ( parse_tree_string_to_values( ln ) for ln in
		filter( non_empty_line, imap( remove_comments, parse_tree_in_fl ) ) )

	cpp_out_fl.write( env.render_exe( values ) )

