# Copyright (C) 2011-2013 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

# I call on you, my God, for you will answer me; turn your ear to me and
# hear my prayer. Psalm 17 v6

from abc import ABCMeta
from abc import abstractmethod

from libpepper.values import PepValue

class PepCallable( PepValue ):
    @abstractmethod
    def call( self, args, env ): pass

    @abstractmethod
    def return_type( self, args, env ): pass

    @abstractmethod
    def args_match( self, args, env ): pass

