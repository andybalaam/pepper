# Copyright (C) 2011-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


from buildstep import BuildStep

class SourceBuildStep( BuildStep ):
    def read_from_file( self, fl ):
        return fl

    def process( self, inp ):
        raise AssertionError( "Can't process into source file" )

    def write_to_file( self, fl ):
        raise AssertionError( "Can't write source file" )

