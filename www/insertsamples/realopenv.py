
import os.path
import sys

from import openv import OpEnv

class RealOpEnv( OpEnv ):

	def main_input_file( self ):
		return sys.stdin

	def main_output_file( self ):
		return sys.stdout

	def path_exists( self, filename ):
		return os.path.exists( filename )

	def open_file( self, filename, rw ):
		if rw == "w":
			dr = os.path.dirname( filename )
			if not os.path.isdir( dr ):
				os.makedirs( dr )
		return open( filename, rw )
