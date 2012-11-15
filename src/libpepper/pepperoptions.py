# Copyright (C) 2011-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


import version

from optparse import OptionParser

from usererrorexception import PepUserErrorException

class PepperOptions( object ):

    SOURCE = 0
    LEXED  = 1
    PARSED = 2
    CPP    = 3
    EXE    = 4
    RUN    = 5

    USAGE = """%prog [options] input_file [arg1 ...]"""

    VERSION = "%prog " + version.VERSION

    EXT2TYPE = {
        ".pepper"       : SOURCE,
        ".pepperlexed"  : LEXED,
        ".pepperparsed" : PARSED,
        ".cpp"          : CPP,
        }

    class FileDetails( object ):

        def __init__( self, filename ):
            self.filetype = self.filename2filetype( filename )
            self.filename = filename

        def filename2filetype( self, filename ):
            for ext, tp in PepperOptions.EXT2TYPE.items():
                if filename.endswith( ext ):
                    return tp
            return PepperOptions.EXE

    class RunFileDetails( object ):
        def __init__( self ):
            self.filetype = PepperOptions.RUN

    def __init__( self, argv ):
        parser = OptionParser(
            usage   = PepperOptions.USAGE,
            version = PepperOptions.VERSION,
            prog = argv[0],
            )

        parser.add_option( "-o", "--outfile", dest="outfile",
            help="Store the output to the supplied file." )

        (options, args) = parser.parse_args( argv[1:] )

        if len( args ) < 1:
            raise PepUserErrorException( parser.get_usage() )

        self.infile  = PepperOptions.FileDetails( args[0] )

        if options.outfile:
            self.outfile = PepperOptions.FileDetails( options.outfile )
        else:
            self.outfile = PepperOptions.RunFileDetails()

        self.args = args[1:]

