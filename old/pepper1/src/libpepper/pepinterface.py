# Copyright (C) 2011-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


def implements_interface( obj, interface ):
    if str( interface ) == "<class 'libpepper.values.PepSymbol'>":
        return str( obj.__class__ ) != "<class 'libpepper.vals.basic_types.pepvariable.PepVariable'>"
    return True # TODO: check we implement it
