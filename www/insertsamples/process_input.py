#!/usr/bin/env python

import re

eeyore_re = re.compile( "eeyore::(.*)" )


def asciidoc_filename( sample_name ):
	return "asciidoc/samples/{sn}/{sn}.asciidoc".format( sn = sample_name )

def sample_filename( sample_name, ext ):
	return "samples/{sn}/{sn}.{ext}".format( sn = sample_name, ext = ext )

def write_sample_results( sample_name, test_results, oe ):
	out_filename = asciidoc_filename( sample_name )
	with oe.open_file( out_filename, "w" ) as out_file:
		pass

def run_sample( sample_name, from_ext, to_ext, oe ):
	fr_filename = sample_filename( sample_name, from_ext )
	to_filename = sample_filename( sample_name, to_ext )
	if oe.path_exists( fr_filename ) and oe.path_exists( to_filename ):
		with oe.open_file( fr_filename, "r" ) as fr_file:
			with oe.open_file( to_filename, "r" ) as to_file:
				pass


def process_sample( sample_name, oe ):
	test_results = run_sample( sample_name, "eeyore", "cpp", oe )
	write_sample_results( sample_name, test_results, oe )

def process_line( ln, oe ):
	ln = ln.strip()
	m = eeyore_re.match( ln )
	if m:
		process_sample( m.group( 1 ), oe )
		return True
	return False

def process_input( oe ):
	for ln in eo.main_input_file():
		if not process_line( ln, oe ):
			eo.main_output_file().write( ln )


