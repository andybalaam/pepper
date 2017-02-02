# Copyright (C) 2014 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

# Must I wait, now that they are silent, now that they
# stand there with no reply?
# Job 32 v16

from libpepper.vals.functions.pepfunction import PepFunction
#from libpepper.values import PepValue

class PepNow( PepFunction ):

    def construction_args( self ):
        return ()

    def check_one_arg( self, args ):
        if( len( args ) != 1 ):
            raise UserErrorException(
                "There should only ever be one argument to now()" )

    def call( self, args, env ):
        self.check_one_arg( args )
        # This should be the only place in the code where evaluate()
        # is called on something that is not a language-y thing like
        # a type or function, except when we are already inside a
        # call to evaluate().
        ret = args[0].evaluate( env )
        if not ret.is_known( env ):
            raise UserErrorException( "Argument to now() is not known!" )
        return ret

    def return_type( self, args, env ):
        self.check_one_arg( args )
        return args[0].evaluated_type( env )

    def args_match( self, args, env ):
        self.check_one_arg( args )
        return True  # Any type of thing can be passed to now()

