
import version

from optparse import OptionParser

from usererrorexception import EeyUserErrorException

class EeyoreOptions( object ):

    SOURCE     = 0
    LEXED      = 1
    PARSE_TREE = 2
    CPP        = 3
    EXE        = 4

    USAGE = """%prog input_file output_file"""

    VERSION = "%prog " + version.VERSION

    EXT2TYPE = {
        ".eeyore"          : SOURCE,
        ".eeyorelexed"     : LEXED,
        ".eeyoreparsetree" : PARSE_TREE,
        ".cpp"             : CPP,
        }

    class FileDetails( object ):

        def __init__( self, filename ):
            self.filetype = self.filename2filetype( filename )
            self.filename = filename

        def filename2filetype( self, filename ):
            for ext, tp in EeyoreOptions.EXT2TYPE.items():
                if filename.endswith( ext ):
                    return tp
            return EeyoreOptions.EXE

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

