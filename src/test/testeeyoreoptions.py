# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


from nose.tools import *

from libeeyore.eeyoreoptions import EeyoreOptions

from libeeyore.usererrorexception import EeyUserErrorException

@raises( EeyUserErrorException )
def test_no_args():
    EeyoreOptions( [ "progname" ] )

def test_one_arg():
    opts = EeyoreOptions( [ "progname", "infile.eeyore" ] )

    assert_equal( opts.infile.filetype, EeyoreOptions.SOURCE )
    assert_equal( opts.infile.filename, "infile.eeyore" )

    assert_equal( opts.outfile.filetype, EeyoreOptions.RUN )


def test_parse_to_cpp():
    opts = EeyoreOptions(
        [ "progname", "-o", "outfile.cpp", "infile.eeyoreparsed" ] )

    assert_equal( opts.infile.filetype, EeyoreOptions.PARSED )
    assert_equal( opts.infile.filename, "infile.eeyoreparsed" )

    assert_equal( opts.outfile.filetype, EeyoreOptions.CPP )
    assert_equal( opts.outfile.filename, "outfile.cpp" )

def test_eeyore_to_lexed():
    opts = EeyoreOptions(
        [ "progname", "--outfile", "outfile.eeyorelexed", "infile.eeyore" ] )

    assert_equal( opts.infile.filetype, EeyoreOptions.SOURCE )
    assert_equal( opts.infile.filename, "infile.eeyore" )

    assert_equal( opts.outfile.filetype, EeyoreOptions.LEXED )
    assert_equal( opts.outfile.filename, "outfile.eeyorelexed" )


def test_eeyore_to_exe():
    opts = EeyoreOptions(
        [ "progname", "-o", "outfile", "infile.eeyore" ] )

    assert_equal( opts.infile.filetype, EeyoreOptions.SOURCE )
    assert_equal( opts.infile.filename, "infile.eeyore" )

    assert_equal( opts.outfile.filetype, EeyoreOptions.EXE )
    assert_equal( opts.outfile.filename, "outfile" )


def test_run_with_args():
    opts = EeyoreOptions(
        [ "progname", "infile.eeyore", "arg1", "arg2" ] )

    assert_equal( opts.infile.filetype, EeyoreOptions.SOURCE )
    assert_equal( opts.infile.filename, "infile.eeyore" )

    assert_equal( opts.outfile.filetype, EeyoreOptions.RUN )

    assert_equal( opts.args, [ "arg1", "arg2" ] )


