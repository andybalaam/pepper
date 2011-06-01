
from nose.tools import *

from libeeyore.eeyoreoptions import EeyoreOptions

from libeeyore.usererrorexception import EeyUserErrorException

@raises( EeyUserErrorException )
def test_no_args():
	EeyoreOptions( [ "progname" ] )

@raises( EeyUserErrorException )
def test_one_arg():
	EeyoreOptions( [ "progname", "infile.eeyoreparsetree" ] )

def test_two_args():
	opts = EeyoreOptions(
		[ "progname", "infile.eeyoreparsetree", "outfile.cpp" ] )

	assert_equal( opts.infile.filetype, EeyoreOptions.PARSE_TREE )
	assert_equal( opts.infile.filename, "infile.eeyoreparsetree" )

	assert_equal( opts.outfile.filetype, EeyoreOptions.CPP )
	assert_equal( opts.outfile.filename, "outfile.cpp" )


