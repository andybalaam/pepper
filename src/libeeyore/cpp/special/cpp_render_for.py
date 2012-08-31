from libeeyore.cpp.cpputils import render_statements

def render_EeyFor( value, env ):

    evald_it = value.iterator.evaluate( env )

    if not evald_it.is_known( env ):
        raise Exception(
            "At the moment, iterators must be known at compile time." ) # TODO

    if evald.evaluated_type() is not EeyRange:
        raise Exception( "Can only iterate over ranges so far." ) # TODO

    # TODO: Only handles numeric values so far, and only incrementing the
    #       iteration variable.

    return """for( {variable_type} {variable_name} = {begin}; {variable_name} < {end}; ++{variable_name} )
{{
    {body_statements}
}}""".format(
        variable_type = value.variable_type.render( env ),
        variable_name = value.variable_name.render( env ),
        begin = value.iterator.begin,
        end = value.iterator.end,
        body_statements = render_statements( value, "        ", env )
    )

    return """if( {predicate} )
    {{
        {cmds_if_true};
    }}{else_block}""".format(
        predicate = value.predicate.render( env ),
        cmds_if_true = _render_cmds( value.cmds_if_true,  env ),
        else_block = else_block
        )

