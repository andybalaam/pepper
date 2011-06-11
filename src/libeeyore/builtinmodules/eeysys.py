
from libeeyore.values import EeyString

_module_prefix = "sys."

_copyright = EeyString(
	"Copyright (C) 2011 Andy Balaam and the Eeyore developers" )

def _add_name( env, name, value ):
	env.namespace[_module_prefix + name] = value

def add_names( env ):
	_add_name( env, "copyright", _copyright )

