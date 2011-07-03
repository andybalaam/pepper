from abc import ABCMeta, abstractmethod

class BuildStep( object ):
    __metaclass__ = ABCMeta

    @abstractmethod
    def read_from_file( self, fl ): pass

    @abstractmethod
    def process( self, inp ): pass

    @abstractmethod
    def write_to_file( self, val, fl ): pass

