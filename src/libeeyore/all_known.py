
def all_known( values, env ):
    return all( map( lambda v: v.is_known( env ), values ) )

