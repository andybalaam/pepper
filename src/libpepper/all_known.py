# Copyright (C) 2011-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


def all_known( values, env ):
    return all( map( lambda v: v.is_known( env ), values ) )

