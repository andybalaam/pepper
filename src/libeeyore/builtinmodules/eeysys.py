
from libeeyore.values import EeyString
from libeeyore.values import EeyValue

_module_prefix = "sys."

_copyright = EeyString(
    "Copyright (C) 2011 Andy Balaam and the Eeyore developers" )

class EeySysArgv( EeyValue ):

    def __init__( self ):
        EeyValue.__init__( self )

    def construction_args( self ):
        return ()

    def is_known( self, env ):
        False

    def lookup( self, env ):
        return self

_argv = EeySysArgv()

def _add_name( env, name, value ):
    env.namespace[_module_prefix + name] = value

def add_names( env ):
    _add_name( env, "argv",      _argv )
    _add_name( env, "copyright", _copyright )

