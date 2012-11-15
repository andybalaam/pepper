# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


import os
import re
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
    ".eeyoreparsed",
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



class iterate_commands( object ):
    def __init__( self, fl ):
        self.fl = fl
        self.cached_line = None

    def __iter__( self ):
        return self

    def next( self ):

        if self.cached_line is None:
            cmd_line = self.fl.next()
        else:
            cmd_line = self.cached_line

        expected_stdout = ""

        while True:
            try:
                ln = self.fl.next()
            except StopIteration:
                self.cached_line = None
                return cmd_line, expected_stdout

            if ln.startswith( "$" ):
                self.cached_line = ln
                return cmd_line, expected_stdout
            else:
                expected_stdout += ln



class RunEeyoreTest( unittest.TestCase ):

    retval_re = re.compile( r"\s*\[\s*retval\s*=\s*(\d+)\s*\]\s*\n(.*)",
        re.DOTALL )
    stderr_re = re.compile( r"\s*\[\s*stderr\s*\](.*)" )

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
            for cmd_line, expected_stdout in iterate_commands( fl ):
                self.runSingleProgram( cmd_line, expected_stdout )


    def runSingleProgram( self, cmd_line, expected_stdout ):
        expected_retval, expected_stdout, expected_stderr = (
            self.extractExpected( expected_stdout ) )

        assert cmd_line.startswith( "$" )
        cmd_line = cmd_line[1:].strip()

        args = shlex.split( cmd_line )
        ret, out, err = run_cmd( args, self.path )

        assert ret == expected_retval, (
            '"%s" should return %s but returned %d' % (
                cmd_desc( args ), expected_retval, ret ) )

        assert out.strip() == expected_stdout.strip(), (
            '"%s" should print:\n%s' +
            '\nbut instead it printed:\n%s' ) % (
                cmd_desc( args ),
                expected_stdout,
                out )

        assert err.strip() == expected_stderr.strip(), (
            '"%s" should print:\n%s' +
            '\nto stderr but instead it printed:\n%s' ) % (
                cmd_desc( args ),
                expected_stderr,
                err )


    def generateFile( self ):
        """Check that running eeyore on input file returns output file.
        """

        with temp_out_file( "this", ext( self.to_filename ) ) as outfile:
            args = ( "eeyore", "-o", outfile.name, self.from_filename )
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

    def extractExpected( self, expected_stdout ):
        expected_retval = 0
        m = RunEeyoreTest.retval_re.match( expected_stdout )
        if m:
            expected_retval = int( m.group( 1 ) )
            expected_stdout = m.group( 2 )

        expected_stdout, expected_stderr = self.extractStdErrLines(
            expected_stdout )

        return ( expected_retval, expected_stdout, expected_stderr )

    def extractStdErrLines( self, expected_stdout ):
        out_lines = []
        err_lines = []
        for ln in expected_stdout.split( '\n' ):
            m = RunEeyoreTest.stderr_re.match( ln )
            if m:
                err_lines.append( m.group( 1 ) )
            else:
                out_lines.append( ln )
        return '\n'.join( out_lines ), '\n'.join( err_lines )



class EeyoreSampleNosePlugin( Plugin ):
    """
    Find eeyore code samples and run them as tests.
    If a directory contains 2 or more files with extensions from this list:
      .eeyore
      .eeyorelexed
      .eeyoreparsed
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

