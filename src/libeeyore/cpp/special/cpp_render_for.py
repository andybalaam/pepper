from libeeyore.vals.all_values import *

from libeeyore.cpp.cpputils import render_statements

def render_EeyFor( value, env ):
    evald_it = value.iterator.evaluate( env )

    if evald_it.evaluated_type( env ).value is not EeyRange:
        # TODO Can only iterate over ranges
        raise Exception( "Can only iterate over ranges so far, not " +
             str( evald_it.evaluated_type( env ).value ) + "." )

    # TODO: Only handles numeric values so far, and only incrementing the
    #       iteration variable.

    arg_types_and_names = ( ( value.variable_type, value.variable_name ), )
    args = ( value.variable_name, )
    newenv = execution_environment( arg_types_and_names, args, False, env )

    if evald_it.step.evaluate( env ).value == "1":
        modify_code = "++{variable_name}"
    else:
        modify_code = "{variable_name} += {step}"

    modify_code = modify_code.format(
        variable_name = value.variable_name.symbol_name,
        step = evald_it.step.render( env ),
    )

    return """for( {variable_type} {variable_name} = {begin}; {variable_name} < {end}; {modify_code} )
    {{
{body_statements}    }}""".format(
        modify_code = modify_code,
        variable_type = value.variable_type.render( env ),
        variable_name = value.variable_name.symbol_name,
        begin = evald_it.begin.render( env ),
        end   = evald_it.end.render( env ),
        body_statements = render_statements(
            value.body_stmts, "        ", newenv )
    )


