# Copyright (C) 2012-2013 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

# Then the Lord God formed a manfrom the dust of the ground and breathed into
# his nostrils the breath of life, and the man became a living being.
# Genesis 2 v7

from itertools import ifilter

from libpepper.functionvalues import PepDef
from libpepper.languagevalues import PepInit
from libpepper.values import PepSymbol
from libpepper.values import PepType
from libpepper.values import PepVoid

from pepvar import PepVar

from libpepper.usererrorexception import PepUserErrorException

class PepDefInit( PepDef ):
    """
    The value created when a def_init is parsed in source code.
    A def_init may contain one or more var declarations, so we can query
    this object to find what member variables the containing class will have.
    The base class, PepDef contains most of the functionality that allows
    this to be called like any other function.
    """

    INIT_IMPL_NAME = "__init__"

    def __init__( self, arg_types_and_names, body_stmts ):
        PepDef.__init__(
            self,
            PepType( PepVoid ),
            PepSymbol( self.INIT_IMPL_NAME ),
            arg_types_and_names,
            body_stmts
        )
        # TODO: check there is at least one arg
        # TODO: check first arg accepts this class?

    def construction_args( self ):
        return ( self.arg_types_and_names, self.body_stmts )

    def get_member_variables( self, env ):
        ret = []

        is_var = lambda stmt: stmt.__class__ == PepVar
        for var_stmt in ifilter( is_var, self.body_stmts ):
            for init_stmt in var_stmt.body_stmts:
                if init_stmt.__class__ != PepInit:
                    # Should not happen since this is defined in the syntax
                    # (but might change one day?)
                    raise PepUserErrorException(
                        "Var blocks may only contain initialisation statements"
                    )
                # TODO: handle expressions that evaluate to symbols
                nm = init_stmt.var_name.name()
                selfdot = self.self_var_name() + "."
                if not nm.startswith( selfdot ):
                    raise PepUserErrorException(
                        "Only members of this class should be initialised in " +
                        "var blocks.  '" + nm + "' does not start with '" +
                        selfdot + "', but it should."
                    )
                nm = nm[ len(selfdot): ]

                if len( nm ) == 0:
                    raise PepUserErrorException(
                        "You must provide a variable name, not just '" +
                        selfdot + "'."
                    )

                ret.append( ( init_stmt.var_type.evaluate( env ), nm ) )

        return ret

    def self_var_name( self ):
        return self.arg_types_and_names[0][1].name()

