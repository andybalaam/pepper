
import cmd_runner
import cpp_compiler
import parse_tree_to_cpp
import source_to_exe
import source_to_lexed

from eeyoreoptions import EeyoreOptions
from usererrorexception import EeyUserErrorException

from buildsteps.sourcebuildstep  import SourceBuildStep
from buildsteps.lexbuildstep     import LexBuildStep
from buildsteps.parsebuildstep   import ParseBuildStep
from buildsteps.renderbuildstep  import RenderBuildStep

RET_SUCCESS    = 0
RET_USER_ERROR = 1

class Executor( object ):
    def __init__( self ):
        self.build_steps = [
            SourceBuildStep(),   # EeyoreOptions.SOURCE     = 0
            LexBuildStep(),      # EeyoreOptions.LEXED      = 1
            ParseBuildStep(),    # EeyoreOptions.PARSE_TREE = 2
            RenderBuildStep(),   # EeyoreOptions.CPP        = 3
            ]

class FileOperations( object ):
    def open_read( self, filename ):
        return open( filename, "r" )

    def open_write( self, filename ):
        return open( filename, "w" )

def process_options( opts, fl_op, executor ):

    inf = opts.infile
    ouf = opts.outfile

    assert( inf.filetype < ouf.filetype ) # TODO: proper error message

    with fl_op.open_read( inf.filename ) as in_fl:
        step = executor.build_steps[inf.filetype]
        val = step.read_from_file( in_fl )
        for i in range( inf.filetype + 1,
                min( EeyoreOptions.EXE, ouf.filetype + 1 ) ):
            step = executor.build_steps[i]
            val = step.process( val )
            if i == ouf.filetype:
                with fl_op.open_write( ouf.filename ) as out_fl:
                    step.write_to_file( val, out_fl )

        if ouf.filetype == EeyoreOptions.EXE:
            cpp_compiler.run( val, ouf_filename )
        elif ouf.filetype == EeyoreOptions.RUN:
            # TODO: make tmp dir and contruct filename
            cpp_compiler.run( val, "./a.out" )
            return cmd_runner.run( "./a.out" ) # TODO: pass through argv

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



