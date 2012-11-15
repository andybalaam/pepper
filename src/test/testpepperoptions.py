# Copyright (C) 2011-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


from nose.tools import *

from libpepper.pepperoptions import PepperOptions

from libpepper.usererrorexception import EeyUserErrorException

@raises( EeyUserErrorException )
def test_no_args():
    PepperOptions( [ "progname" ] )

def test_one_arg():
    opts = PepperOptions( [ "progname", "infile.pepper" ] )

    assert_equal( opts.infile.filetype, PepperOptions.SOURCE )
    assert_equal( opts.infile.filename, "infile.pepper" )

    assert_equal( opts.outfile.filetype, PepperOptions.RUN )


def test_parse_to_cpp():
    opts = PepperOptions(
        [ "progname", "-o", "outfile.cpp", "infile.pepperparsed" ] )

    assert_equal( opts.infile.filetype, PepperOptions.PARSED )
    assert_equal( opts.infile.filename, "infile.pepperparsed" )

    assert_equal( opts.outfile.filetype, PepperOptions.CPP )
    assert_equal( opts.outfile.filename, "outfile.cpp" )

def test_pepper_to_lexed():
    opts = PepperOptions(
        [ "progname", "--outfile", "outfile.pepperlexed", "infile.pepper" ] )

    assert_equal( opts.infile.filetype, PepperOptions.SOURCE )
    assert_equal( opts.infile.filename, "infile.pepper" )

    assert_equal( opts.outfile.filetype, PepperOptions.LEXED )
    assert_equal( opts.outfile.filename, "outfile.pepperlexed" )


def test_pepper_to_exe():
    opts = PepperOptions(
        [ "progname", "-o", "outfile", "infile.pepper" ] )

    assert_equal( opts.infile.filetype, PepperOptions.SOURCE )
    assert_equal( opts.infile.filename, "infile.pepper" )

    assert_equal( opts.outfile.filetype, PepperOptions.EXE )
    assert_equal( opts.outfile.filename, "outfile" )


def test_run_with_args():
    opts = PepperOptions(
        [ "progname", "infile.pepper", "arg1", "arg2" ] )

    assert_equal( opts.infile.filetype, PepperOptions.SOURCE )
    assert_equal( opts.infile.filename, "infile.pepper" )

    assert_equal( opts.outfile.filetype, PepperOptions.RUN )

    assert_equal( opts.args, [ "arg1", "arg2" ] )


