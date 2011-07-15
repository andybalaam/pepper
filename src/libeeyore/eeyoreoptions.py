
import version

from optparse import OptionParser

from usererrorexception import EeyUserErrorException

class EeyoreOptions( object ):

    SOURCE = 0
    LEXED  = 1
    PARSED = 2
    CPP    = 3
    EXE    = 4
    RUN    = 5

    USAGE = """%prog input_file output_file"""

    VERSION = "%prog " + version.VERSION

    EXT2TYPE = {
        ".eeyore"       : SOURCE,
        ".eeyorelexed"  : LEXED,
        ".eeyoreparsed" : PARSED,
        ".cpp"          : CPP,
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

    class RunFileDetails( object ):
        def __init__( self ):
            self.filetype = EeyoreOptions.RUN

    def __init__( self, argv ):
        parser = OptionParser(
            usage   = EeyoreOptions.USAGE,
            version = EeyoreOptions.VERSION,
            prog = argv[0],
            )

        (options, args) = parser.parse_args( argv[1:] )

        lenargs = len( args )
        if lenargs == 2:
            self.infile  = EeyoreOptions.FileDetails( args[0] )
            self.outfile = EeyoreOptions.FileDetails( args[1] )
        elif lenargs == 1:
            self.infile  = EeyoreOptions.FileDetails( args[0] )
            self.outfile = EeyoreOptions.RunFileDetails()
        else:
            raise EeyUserErrorException( parser.get_usage() )

