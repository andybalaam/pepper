# Copyright (C) 2011-2013 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

# This made the king so angry and furious that he ordered the execution
# of all the wise men of Babylon. Daniel 2 v12

from libpepper.vals.basic_types.pepvariable import PepVariable

def _has_default( type_and_name ):
    return ( len( type_and_name ) == 3 )

def execution_environment( arg_types_and_names, args, known, env ):
    newenv = env.clone_deeper()

    i = 0
    while i < len( arg_types_and_names ):
        type_and_name = arg_types_and_names[i]
        name = type_and_name[1]

        if i < len( args ):
            val = args[i]
        else:
            assert _has_default( type_and_name )
            val = type_and_name[2]

        if known:
            val = val#.evaluate( env )
        else:
            if i < len( args ):
                tp = args[i].evaluated_type( newenv )

                # TODO: imports here to avoid circular deps
                from libpepper.vals.types import PepUserClass
                from libpepper.vals.types import PepConstructingUserClass

                # TODO: this seems like a hack to me.  Can we make
                #       the evaluated type of args[i] just be the
                #       right type (PepConstructingUserClass) already?
                #       If so, we probably do it in cpprenderer.add_def_init.
                if (
                    tp.__class__ == PepUserClass and
                    type_and_name[0].__class__ == PepConstructingUserClass
                ):
                    tp = PepConstructingUserClass( tp )

            else:
                tp  = type_and_name[0]
            val = PepVariable( tp.evaluate( env ), name.name() )

        newenv.namespace[name.name()] = val
        i += 1

    return newenv
