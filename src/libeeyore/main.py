
import parse_tree_to_cpp

from eeyoreoptions import EeyoreOptions
from usererrorexception import EeyUserErrorException

RET_SUCCESS    = 0
RET_USER_ERROR = 1

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
	else:
		raise EeyUserErrorException(
			"Could not auto-recognise the file extensions you supplied," +
			" or they are not supported as input and output types." )

	return RET_SUCCESS


def parse_and_process_options( argv, options_Class, fileops_Class, exec_Class,
		stderr ):

	try:

		options = options_Class( argv )
		file_operations = fileops_Class()
		executor = exec_Class()

		return process_options( options, file_operations, executor )

	except EeyUserErrorException, e:
		stderr.write( str( e ) + "\n" )
		return RET_USER_ERROR

def main( argv, stderr ):

	return parse_and_process_options( argv, EeyoreOptions, FileOperations,
		Executor, stderr )


