# Copyright (C) 2011-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

from abc import ABCMeta, abstractmethod

class BuildStep( object ):
    __metaclass__ = ABCMeta

    @abstractmethod
    def read_from_file( self, fl ): pass

    @abstractmethod
    def process( self, inp ): pass

    @abstractmethod
    def write_to_file( self, val, fl ): pass

