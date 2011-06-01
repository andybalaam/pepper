
import parse_tree_to_cpp

from eeyoreoptions import EeyoreOptions

class Executor( object ):
	def parse_tree_to_cpp( self, parse_tree_in_fl, cpp_out_fl ):
		parse_tree_to_cpp.parse_tree_to_cpp( parse_tree_in_fl, cpp_out_fl )

class FileOperations( object ):
	def open_read( self, filename ):
		return open( filename, "r" )

	def open_write( self, filename ):
		return open( filename, "w" )


def process_options( opts, fl_op, executor ):

	inf = opts.infile
	ouf = opts.outfile

	if ( inf.filetype == EeyoreOptions.PARSE_TREE and
			ouf.filetype == EeyoreOptions.CPP ):
		with fl_op.open_read( inf.filename ) as in_fl:
			with fl_op.open_write( ouf.filename ) as out_fl:
				executor.parse_tree_to_cpp( in_fl, out_fl )

def main( argv ):

	options = EeyoreOptions( argv )
	file_operations = FileOperations()
	executor = Executor()

	process_options( options, file_operations, executor )

