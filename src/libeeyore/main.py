# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


import os
import os.path
import subprocess

import cpp.cmdrunner
import cpp.cppcompiler

from eeyoreoptions import EeyoreOptions
from usererrorexception import EeyUserErrorException

from buildsteps.sourcebuildstep  import SourceBuildStep
from buildsteps.lexbuildstep     import LexBuildStep
from buildsteps.parsebuildstep   import ParseBuildStep
from buildsteps.renderbuildstep  import RenderBuildStep

RET_SUCCESS    = 0
RET_USER_ERROR = 1

class Executor( object ):
    def __init__( self, sys_op ):
        self.build_steps = [
            SourceBuildStep(),   # EeyoreOptions.SOURCE = 0
            LexBuildStep(),      # EeyoreOptions.LEXED  = 1
            ParseBuildStep(),    # EeyoreOptions.PARSED = 2
            RenderBuildStep(),   # EeyoreOptions.CPP    = 3
            ]
        self.cppcompiler = cpp.cppcompiler.CppCompiler( sys_op )
        self.cmdrunner   = cpp.cmdrunner.CmdRunner( sys_op )

class SystemOperations( object ):
    def open_read( self, filename ):
        return open( filename, "r" )

    def open_write( self, filename ):
        return open( filename, "w" )

    def Popen( self, args, stdin = None, stdout = None, stderr = None ):
        return subprocess.Popen( args, stdin=stdin, stdout=stdout,
            stderr=stderr )

    def isdir( self, path ):
        return os.path.isdir( path )

    def makedirs( self, path ):
        return os.makedirs( path )


TEMP_DIR = ".eeyore"

def _temp_dir_file( sys_op, filename ):
    """Create the temp dir if necessary, and return the path to the supplied
    filename in the temp dir."""
    # TODO: make the dir near the .eeyore file if possible, or in /tmp
    # otherwise?
    if not sys_op.isdir( TEMP_DIR ):
        sys_op.makedirs( TEMP_DIR )
    return os.path.join( TEMP_DIR, filename )

def _exe_name( in_filename ):
    doti = in_filename.rfind( "." )
    if doti == -1:
        return in_filename
    else:
        return in_filename[:doti]

def process_options( opts, sys_op, executor ):

    inf = opts.infile
    ouf = opts.outfile

    assert( inf.filetype < ouf.filetype ) # TODO: proper error message

    with sys_op.open_read( inf.filename ) as in_fl:
        step = executor.build_steps[inf.filetype]
        val = step.read_from_file( in_fl )
        for i in range( inf.filetype + 1,
                min( EeyoreOptions.EXE, ouf.filetype + 1 ) ):
            step = executor.build_steps[i]
            val = step.process( val )
            if i == ouf.filetype:
                with sys_op.open_write( ouf.filename ) as out_fl:
                    step.write_to_file( val, out_fl )

        if ouf.filetype == EeyoreOptions.EXE:
            executor.cppcompiler.run( val, ouf.filename )
        elif ouf.filetype == EeyoreOptions.RUN:
            out_fn = _temp_dir_file( sys_op, _exe_name( inf.filename ) )
            executor.cppcompiler.run( val, out_fn )
            return executor.cmdrunner.run( out_fn, opts.args )

    return RET_SUCCESS


def parse_and_process_options( argv, options_Class, sysops_Class, exec_Class,
        stderr ):

    try:

        options = options_Class( argv )
        sys_operations = sysops_Class()
        executor = exec_Class( sys_operations )

        return process_options( options, sys_operations, executor )

    except EeyUserErrorException, e:
        stderr.write( "Error: " + str( e ) + "\n" )
        return RET_USER_ERROR

def main( argv, stderr ):

    return parse_and_process_options( argv, EeyoreOptions, SystemOperations,
        Executor, stderr )



