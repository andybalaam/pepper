
import os
import shlex
import subprocess
import tempfile
import unittest

from collections import defaultdict

from nose.plugins.base import Plugin

def split_ext( filename ):
    i = filename.rfind( "." )
    if i == -1:
        return ( filename, "" )
    else:
        return ( filename[:i], filename[i:] )


def ext( filename ):
    i = filename.rfind( "." )
    if i == -1:
        return ""
    else:
        return filename[i:]

extns = (
    ".eeyore",
    ".eeyorelexed",
    ".eeyoreparsetree",
    ".cpp",
    ".output"
    )

ext2idx = dict( ( ( ext, extns.index( ext ) ) for ext in extns ) )

def sort_in_extension_order( files ):
    files.sort( key = lambda ext_fn: ext2idx[ ext_fn[0] ] )



def read_file( filename ):
	with open( filename, "r" ) as fl:
		return fl.read()

def temp_out_file( prefix, suffix = "" ):
	return tempfile.NamedTemporaryFile( mode="w", prefix="s2a" + prefix,
		suffix = suffix )

def run_cmd( args, cwd ):
	"""Runs a command and returns its return code, its standard output and its
	standard error."""

	with temp_out_file( "out" ) as stdoutfl:
		with temp_out_file( "err" ) as stderrfl:
			retval = subprocess.call( args=args, stdout=stdoutfl,
				stderr=stderrfl, cwd=cwd )
			stdout = read_file( stdoutfl.name )
			stderr = read_file( stderrfl.name )

	return ( retval, stdout, stderr )


def cmd_desc( args, repl = None ):
    if repl is not None:
        args = ( a if i is not repl[0] else repl[1]
            for i, a in enumerate( args ) )
    return "$ %s" % " ".join( args )

class RunEeyoreTest( unittest.TestCase ):
    def __init__( self, path, from_filename, to_filename ):

        if to_filename.endswith( ".output" ):
            methodName = "runProgram"
        else:
            methodName = "generateFile"

        unittest.TestCase.__init__( self, methodName )
        self.path = path
        self.from_filename = from_filename
        self.to_filename   = to_filename

    def runProgram( self ):
        """Check that running the supplied program with eeyore prints the
        expected results.
        """

        with open( os.path.join( self.path, self.to_filename ), "r" ) as fl:
            first_line = fl.readline()
            expected_output = fl.read()

        assert first_line.startswith( "$" )
        first_line = first_line[1:].strip()

        args = shlex.split( first_line )
        ret, out, err = run_cmd( args, self.path )

        assert ret == 0, ( '"%s" should return 0 but returned %d' % (
            cmd_desc( args ), ret ) )

        assert out == expected_output, ( '"%s" should print:\n%s' +
                '\nbut instead it printed:\n%s' ) % (
                    cmd_desc( args ),
                    expected_output,
                    out )


    def generateFile( self ):
        """Check that running eeyore on input file returns output file.
        """

        with temp_out_file( "this", ext( self.to_filename ) ) as outfile:
            args = ( "eeyore", self.from_filename, outfile.name )
            ret, out, err = run_cmd( args, self.path )
            contents = read_file( outfile.name )

        assert ret == 0, ( '"%s" should return 0 but returned %d' % (
            cmd_desc( args, repl = ( 2, self.to_filename ) ), ret ) )

        expected_contents = read_file( os.path.join(
            self.path, self.to_filename ) )

        assert contents == expected_contents, (
                '"%s" should result in a file containing:\n%s' +
                '\nbut instead it gave:\n%s' ) % (
                    cmd_desc( args, repl = ( 2, self.to_filename ) ),
                    expected_contents,
                    contents )


class EeyoreSampleNosePlugin( Plugin ):
    """
    Find eeyore code samples and run them as tests.
    If a directory contains 2 or more files with extensions from this list:
      .eeyore
      .eeyorelexed
      .eeyoreparsetree
      .cpp
      .output
    with matching names before the extensionm the eeyore executable will be
    run to generate each file from the previous one, and the output will be
    required to match that specified.
    Files ending in .output will be matched against the output of running
    eeyore on the first file in found.
    """

    def loadTestsFromDir( self, path ):
        name2files = defaultdict( lambda: [] )
        for filename in os.listdir( path ):
            name, ext = split_ext( filename )
            if ext in extns:
                name2files[name].append( ( ext, filename ) )

        for name, files in name2files.iteritems():
            if len( files ) < 2:
                continue
            sort_in_extension_order( files )
            prev_name = None
            for ext, filename in files:
                if prev_name is not None:
                    yield RunEeyoreTest( path, prev_name, filename )
                prev_name = filename

