# Copyright (C) 2012-2013 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

# For instance, a man may go into the forest with his neighbour to cut wood,
# and as he swings his axe to fell a tree, the head may fly off and hit his
# neighbour and kill him. That man may flee to one of these cities and save
# his life.  Deuteronomy 19 v5

from libpepper.values import PepValue

from pepinstancenamespace import PepInstanceNamespace

class PepInstance( PepValue ):
    """
    An instance of a class - what you get back when you call ClassName.init().
    This is the base class for PepKnownInstance and PepRuntimeInstance.
    It allows bound methods to be returned when we ask for them by name because
    it contains a PepInstanceNamespace instead of a normal namespace.
    """

    def __init__( self, clazz ):
        PepValue.__init__( self )
        self.clazz = clazz
        self.namespace = PepInstanceNamespace(
            self, self.clazz.get_namespace() )

    def get_class_name( self ):
        return self.clazz.name

    def get_namespace( self ):
        return self.namespace

    def evaluated_type( self, env ):
        return self.clazz


