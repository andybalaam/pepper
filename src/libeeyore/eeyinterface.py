
def implements_interface( obj, interface ):
	if str( interface ) == "<class 'libeeyore.values.EeySymbol'>":
		return str( obj.__class__ ) != "<class 'libeeyore.values.EeyVariable'>"
	return True # TODO: check we implement it
