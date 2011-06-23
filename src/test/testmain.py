
from cStringIO import StringIO
from nose.tools import *

from libeeyore.eeyoreoptions import EeyoreOptions
from libeeyore.parse_tree_to_cpp import parse_tree_to_cpp
from libeeyore.source_to_lexed import source_to_lexed
from libeeyore.usererrorexception import EeyUserErrorException

import libeeyore.main

class FakeObject( object ):
	pass

class FakeExecutor( object ):
	def __init__( self ):
		self.calls = []

	def parse_tree_to_cpp( self, parse_tree_in_fl, cpp_out_fl ):
		self.calls.append( "parse_tree_to_cpp(%s,%s)" % (
			str( parse_tree_in_fl ), str( cpp_out_fl ) ) )

	def source_to_lexed( self, source_in_fl, lexed_out_fl ):
		self.calls.append( "source_to_lexed(%s,%s)" % (
			str( source_in_fl ), str( lexed_out_fl ) ) )

class IdentifiableFakeFile( object ):
	def __init__( self, name ):
		self.name = name

	def __enter__( self ):
		return self

	def __exit__( self, arg1, arg2, arg3 ):
		pass

	def __str__( self ):
		return self.name

class FakeFileOperations( object ):
	def __init__( self ):
		self.calls = []

	def open_read( self, filename ):
		self.calls.append( "open_read(%s)" % filename )
		return IdentifiableFakeFile( "r" )

	def open_write( self, filename ):
		self.calls.append( "open_write(%s)" % filename )
		return IdentifiableFakeFile( "w" )

class FakeOptions( object ):
	def __init__( self, argv ):
		self.infile = FakeObject()
		self.infile.filetype = EeyoreOptions.PARSE_TREE
		self.infile.filename = "test.eeyoreparsetree"
		self.outfile = FakeObject()
		self.outfile.filetype = EeyoreOptions.CPP
		self.outfile.filename = "test.cpp"

def test_process_options_parse_tree_to_cpp():

	options = FakeOptions( "" )
	file_operations = FakeFileOperations()
	executor = FakeExecutor()

	libeeyore.main.process_options( options, file_operations, executor )

	fo_calls = file_operations.calls
	assert_equal( len( fo_calls ), 2 )

	assert_equal( fo_calls[0], "open_read(test.eeyoreparsetree)" )
	assert_equal( fo_calls[1], "open_write(test.cpp)" )

	assert_equal( executor.calls, ["parse_tree_to_cpp(r,w)"] )


class AlwaysThrowUserErrorOptions( object ):
	def __init__( self, argv ):
		raise EeyUserErrorException( "usage: blah" )

def test_parse_and_process_options_arguments_wrong():

	stderr = StringIO()

	ret = libeeyore.main.parse_and_process_options( [],
		AlwaysThrowUserErrorOptions, FakeObject, FakeObject, stderr )

	assert_equal( stderr.getvalue(), "usage: blah\n" )
	assert_equal( ret, 1 )




def test_parse_and_process_options_arguments_wrong():

	stderr = StringIO()

	ret = libeeyore.main.parse_and_process_options( [],
		FakeOptions, FakeFileOperations, FakeExecutor, stderr )

	assert_equal( stderr.getvalue(), "" )
	assert_equal( ret, 0 )



def test_process_options_source_to_lexed():

	options = FakeOptions( "" )
	options.infile.filetype = EeyoreOptions.SOURCE
	options.infile.filename = "test.eeyore"
	options.outfile.filetype = EeyoreOptions.LEXED
	options.outfile.filename = "test.eeyorelexed"

	file_operations = FakeFileOperations()
	executor = FakeExecutor()

	libeeyore.main.process_options( options, file_operations, executor )

	fo_calls = file_operations.calls
	assert_equal( len( fo_calls ), 2 )

	assert_equal( fo_calls[0], "open_read(test.eeyore)" )
	assert_equal( fo_calls[1], "open_write(test.eeyorelexed)" )

	assert_equal( executor.calls, ["source_to_lexed(r,w)"] )


def test_parse_tree_to_cpp():

	in_fl = StringIO( """

	# Comment
	EeyFunctionCall( EeySymbol( "print" ), ( EeyString( "Hello, world!" ), ) ) #com
	""" )

	out_fl = StringIO()

	parse_tree_to_cpp( in_fl, out_fl )

	assert_equal( out_fl.getvalue(), """#include <stdio.h>

int main( int argc, char* argv[] )
{
	printf( "Hello, world!\\n" );

	return 0;
}
""" )

def test_source_to_lexed():
	in_fl = StringIO( """

	# Comment
print( "Hello, world!" ) # comment 2

	""" )

	out_fl = StringIO()

	source_to_lexed( in_fl, out_fl )

	assert_equal( out_fl.getvalue().strip().split( "\n" ), [
		"0004:0001     SYMBOL(print)",
		"0004:0006     LPAREN",
		"0004:0008     STRING(Hello, world!)",
		"0004:0024     RPAREN",
		] )

