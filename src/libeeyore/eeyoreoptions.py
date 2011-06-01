
import version

from optparse import OptionParser

from usererrorexception import EeyUserErrorException

class EeyoreOptions( object ):

	PARSE_TREE = 0
	CPP        = 1

	USAGE = """%prog input_file output_file"""

	VERSION = "%prog " + version.VERSION

	class FileDetails( object ):
		def __init__( self, filename ):
			self.filetype = self.filename2filetype( filename )
			self.filename = filename

		def filename2filetype( self, filename ):
			if filename.endswith( ".eeyoreparsetree" ):
				return EeyoreOptions.PARSE_TREE
			elif filename.endswith( ".cpp" ):
				return EeyoreOptions.CPP


	def __init__( self, argv ):
		parser = OptionParser(
			usage   = EeyoreOptions.USAGE,
			version = EeyoreOptions.VERSION,
			prog = argv[0],
			)

		(options, args) = parser.parse_args( argv[1:] )

		if len( args ) != 2:
			raise EeyUserErrorException( parser.get_usage() )

		self.infile  = EeyoreOptions.FileDetails( args[0] )
		self.outfile = EeyoreOptions.FileDetails( args[1] )

