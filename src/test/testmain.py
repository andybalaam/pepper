
from cStringIO import StringIO
from nose.tools import *

from libeeyore.eeyoreoptions import EeyoreOptions
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


