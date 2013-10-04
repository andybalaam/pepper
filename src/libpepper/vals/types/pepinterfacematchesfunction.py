# Copyright (C) 2013 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

# He told them this parable: 'No one tears a piece out of a new garment to
# patch an old one. Otherwise, they will have torn the new garment, and the
# patch from the new will not match the old.'  Luke 5 v36

from libpepper.vals.functions.pepfunction import PepFunction
from libpepper.values import PepBool
from libpepper.values import PepType
from libpepper.values import PepValue
from libpepper.values import all_known

from pepuserclass import PepUserClass

class PepInterfaceMatchesFunction( PepFunction ):
    """
    The function created when you ask for MyInterface.matches.
    """

    def __init__( self, user_interface ):
        PepFunction.__init__( self )
        self.user_interface = user_interface
        self.arg_types_and_names = ( ( PepType( PepUserClass ), "class" ), )

    def call( self, args, env ):

        if all_known( args, env ):
            ui = self.user_interface.evaluate( env )
            cl = args[0].evaluate( env )
            return PepBool( ui.can_match( cl, env ) )
        else:
            raise Exception(
                "We don't (yet) allow checking interfaces at runtime." )

    def return_type( self, args, env ):
        return PepType( PepBool )

    def args_match( self, args, env ):
        # TODO: we can re-use the code in PepUserFunction.args_match here,
        #       just as we are to print the error when we fail (it's
        #       printed by PepFunctionOverloadList
        if len( args ) != 1:
            return False
        return args[0].evaluated_type( env ) == PepType( PepUserClass )


    def construction_args( self ):
        return ( self.user_interface, )

