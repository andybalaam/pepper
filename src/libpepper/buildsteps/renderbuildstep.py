# Copyright (C) 2011-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


from buildstep import BuildStep
from libpepper import builtins
from libpepper.cpp.cpprenderer import PepCppRenderer
from libpepper.environment import PepEnvironment

class RenderBuildStep( BuildStep ):
    def read_from_file( self, fl ):
        return fl.read()

    def process( self, val ):
        env = PepEnvironment( PepCppRenderer() )
        builtins.add_builtins( env )
        return env.render_exe( val )

    def write_to_file( self, val, fl ):
        for v in val:
            fl.write( v )

