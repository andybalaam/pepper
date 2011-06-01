from nose.tools import *

from libeeyore.eeyoreoptions import EeyoreOptions
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

def test_process_options_parse_tree_to_cpp():

	options = FakeObject()

	options.infile = FakeObject()
	options.infile.filetype = EeyoreOptions.PARSE_TREE
	options.infile.filename = "test.eeyoreparsetree"

	options.outfile = FakeObject()
	options.outfile.filetype = EeyoreOptions.CPP
	options.outfile.filename = "test.cpp"

	file_operations = FakeFileOperations()
	executor = FakeExecutor()

	libeeyore.main.process_options( options, file_operations, executor )

	fo_calls = file_operations.calls
	assert_equal( len( fo_calls ), 2 )

	assert_equal( fo_calls[0], "open_read(test.eeyoreparsetree)" )
	assert_equal( fo_calls[1], "open_write(test.cpp)" )

	assert_equal( executor.calls, ["parse_tree_to_cpp(r,w)"] )

