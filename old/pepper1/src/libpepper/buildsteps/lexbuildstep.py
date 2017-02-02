# Copyright (C) 2011-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


from buildstep import BuildStep
from parse import PepperLexer
from parse import PepperParser
from parse.peppertokenstreamfromfile import PepperTokenStreamFromFile
from parse.peppertokentostring import render_token
from parse.indentdedenttokenstream import IndentDedentTokenStream

class LexBuildStep( BuildStep ):
    def read_from_file( self, fl ):
        return PepperTokenStreamFromFile( fl )

    def process( self, val ):
        return IndentDedentTokenStream( PepperLexer.Lexer( val ) )

    def write_to_file( self, val, fl ):
        for token in val:
            fl.write( render_token( token ) )
            fl.write( "\n" )

