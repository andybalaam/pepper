from abc import ABCMeta, abstractmethod

class OpEnv:
	"""
	An operating environment: an abstraction of the file and execution
	environment within which we are working.
	"""

	__metaclass__ = ABCMeta

	@abstractmethod
	def main_input_file( self ): pass

	@abstractmethod
	def main_output_file( self ): pass

	@abstractmethod
	def path_exists( self, filename ): pass

	@abstractmethod
	def open_file( self, filename, rw ): pass

