# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

from libeeyore.values import EeyPass

def render_statements( statements, indent, env ):
    ret = ""
    for stmt in statements:
        st = stmt.evaluate( env )
        if st.__class__ is EeyPass:
            continue
        ret += "%s%s;\n" % ( indent, st.render( env ) )
    return ret

