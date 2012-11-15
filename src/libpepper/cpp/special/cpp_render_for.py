# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

from libpepper.vals.all_values import *

from libpepper.cpp.cpputils import render_statements

from libpepper import builtins

def render_PepFor( value, env ):
    evald_it = value.iterator.evaluate( env )

    if evald_it.evaluated_type( env ).value is PepRange:
        if evald_it.__class__ is PepRange:
            step  = evald_it.step
            begin = evald_it.begin
            end   = evald_it.end
        elif (
            evald_it.__class__ is PepRuntimeUserFunction and
            evald_it.user_function is builtins.range_function
        ):
        # TODO: surely there's a cleverer way to do this than knowing the impl
        #       of the range function?
            begin = evald_it.args[0]
            end   = evald_it.args[1]
            if len( evald_it.args ) > 2:
                step = evald_it.args[2]
            else:
                step = PepInt( "1" )
        else:
            # TODO: support evaluating unknown functions that return ranges?
            raise Exception( "Can't (currently) support iterating over " +
                "functions that return ranges." )
    else:
        # TODO Can only iterate over ranges
        raise Exception( "Can only iterate over ranges so far, not " +
             str( evald_it.evaluated_type( env ).value ) + "." )

    # TODO: Only handles numeric values so far, and only incrementing the
    #       iteration variable.

    arg_types_and_names = ( ( value.variable_type, value.variable_name ), )
    args = ( value.variable_name, )
    newenv = execution_environment( arg_types_and_names, args, False, env )

    if step.evaluate( env ).value == "1":
        modify_code = "++{variable_name}"
    else:
        modify_code = "{variable_name} += {step}"

    modify_code = modify_code.format(
        variable_name = value.variable_name.symbol_name,
        step = step.render( env ),
    )

    return """for( {variable_type} {variable_name} = {begin}; {variable_name} < {end}; {modify_code} )
    {{
{body_statements}    }}""".format(
        modify_code = modify_code,
        variable_type = value.variable_type.render( env ),
        variable_name = value.variable_name.symbol_name,
        begin = begin.render( env ),
        end = end.render( env ),
        body_statements = render_statements(
            value.body_stmts, "        ", newenv )
    )


