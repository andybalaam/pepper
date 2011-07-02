
from buildstep import BuildStep
from libeeyore import builtins
from libeeyore.cpp.cpprenderer import EeyCppRenderer
from libeeyore.environment import EeyEnvironment

class RenderBuildStep( BuildStep ):
    def read_from_file( self, fl ):
        raise AssertionError( "Can't read cpp file" )

    def process( self, val ):
        env = EeyEnvironment( EeyCppRenderer() )
        builtins.add_builtins( env )
        return env.render_exe( val )

    def write_to_file( self, val, fl ):
        fl.write( val )

