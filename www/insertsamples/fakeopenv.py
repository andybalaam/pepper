
from cStringIO import StringIO

from openv import OpEnv

class FileLikeContextManager:
	def __init__( self, fakefile ):
		self.fakefile = fakefile
	def __enter__( self ):
		return self.fakefile
	def __exit__( self, exc_type, exc_value, traceback ):
		self.fakefile.close()

class FakeOpEnv( OpEnv ):

	def __init__( self, fakefilenames = () ):
		self.fakefiles = {}
		self.inp_file = StringIO()
		self.out_file = StringIO()
		for filename in fakefilenames:
			self.fakefiles[filename] = StringIO()

	def path_exists( self, filename ):
		return filename in self.fakefiles

	def open_file( self, filename, rw ):
		if rw == "w":
			self.fakefiles[filename] = StringIO()
		return FileLikeContextManager( self.fakefiles[filename] )

	def main_input_file( self ):
		return self.inp_file

	def main_output_file( self ):
		return self.out_file

