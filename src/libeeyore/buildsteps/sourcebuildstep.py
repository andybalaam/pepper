
from buildstep import BuildStep

class SourceBuildStep( BuildStep ):
    def read_from_file( self, fl ):
        return fl

    def process( self, inp ):
        raise AssertionError( "Can't process into source file" )

    def write_to_file( self, fl ):
        raise AssertionError( "Can't write source file" )

