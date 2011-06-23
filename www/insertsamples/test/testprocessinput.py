#!/usr/bin/env python

from nose.tools import *

import process_input

from fakeopenv import FakeOpEnv

def test_run_sample_both_missing():
	oe = FakeOpEnv()
	process_input.run_sample( "sample", "eeyore", "cpp", oe )
	# Nothing was created because the two files don't exist
	assert_equal( len( oe.fakefiles ), 0 )

def test_run_sample_first_missing():
	oe = FakeOpEnv( ( "samples/s/s.cpp", ) )
	process_input.run_sample( "s", "eeyore", "cpp", oe )
	# Nothing was created because the two files don't exist
	assert_equal( len( oe.fakefiles ), 1 )

def test_run_sample_second_missing():
	oe = FakeOpEnv( ( "samples/s/s.eeyore", ) )
	process_input.run_sample( "s", "eeyore", "cpp", oe )
	# Nothing was created because the two files don't exist
	assert_equal( len( oe.fakefiles ), 1 )

def test_run_sample_eeyore_to_cpp():
	eey_fn = "samples/s/s.eeyore"
	cpp_fn = "samples/s/s.cpp"
	oe = FakeOpEnv( ( eey_fn, cpp_fn ) )

	process_input.run_sample( "s", "eeyore", "cpp", oe )

	# eeyore was run with the right arguments
	assert_equal( len( oe.commands ), 1 )
	assert_equal( oe.commands[0], "eeyore" )

	asciidoc_fn = "asciidoc/samples/s/s.asciidoc"
	assert_true( asciidoc_fn in oe.fakefiles )


