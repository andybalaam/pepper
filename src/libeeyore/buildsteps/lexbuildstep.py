
from buildstep import BuildStep
from parse import EeyoreLexer
from parse import EeyoreParser
from parse.eeyoretokenstreamfromfile import EeyoreTokenStreamFromFile
from parse.eeyoretokentostring import render_token

class LexBuildStep( BuildStep ):
    def read_from_file( self, fl ):
        return EeyoreTokenStreamFromFile( fl )

    def process( self, val ):
        return EeyoreLexer.Lexer( val )

    def write_to_file( self, val, fl ):
        for token in val:
            fl.write( render_token( token ) )
            fl.write( "\n" )

