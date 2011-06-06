
import builtins

from cpp.cpprenderer import EeyCppRenderer
from environment import EeyEnvironment
from values import *

def parse_tree_string_to_values( string ):
	return eval( string )

def non_empty_line( ln ):
	return ( ln.strip() != "" )

def parse_tree_to_cpp( parse_tree_in_fl, cpp_out_fl ):
	env = EeyEnvironment( EeyCppRenderer() )
	builtins.add_builtins( self )

	values = ( parse_tree_string_to_values( ln ) for ln in
		filter( non_empty_line, parse_tree_in_fl ) )

	cpp_out_fl.write( env.render_exe( values ) )

