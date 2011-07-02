
from nose.tools import *

from libeeyore.eeyoreoptions import EeyoreOptions

from libeeyore.usererrorexception import EeyUserErrorException

@raises( EeyUserErrorException )
def test_no_args():
    EeyoreOptions( [ "progname" ] )

@raises( EeyUserErrorException )
def test_one_arg():
    EeyoreOptions( [ "progname", "infile.eeyoreparsetree" ] )

def test_parse_to_cpp():
    opts = EeyoreOptions(
        [ "progname", "infile.eeyoreparsetree", "outfile.cpp" ] )

    assert_equal( opts.infile.filetype, EeyoreOptions.PARSE_TREE )
    assert_equal( opts.infile.filename, "infile.eeyoreparsetree" )

    assert_equal( opts.outfile.filetype, EeyoreOptions.CPP )
    assert_equal( opts.outfile.filename, "outfile.cpp" )

def test_eeyore_to_lexed():
    opts = EeyoreOptions(
        [ "progname", "infile.eeyore", "outfile.eeyorelexed" ] )

    assert_equal( opts.infile.filetype, EeyoreOptions.SOURCE )
    assert_equal( opts.infile.filename, "infile.eeyore" )

    assert_equal( opts.outfile.filetype, EeyoreOptions.LEXED )
    assert_equal( opts.outfile.filename, "outfile.eeyorelexed" )


