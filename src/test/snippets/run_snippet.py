# Copyright (C) 2014 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

# Four things on earth are small, yet they are extremely wise:
# Proverbs 30 v24

from cStringIO import StringIO

from libpepper.buildsteps.lexbuildstep import LexBuildStep
from libpepper.buildsteps.parsebuildstep import ParseBuildStep
from libpepper.buildsteps.renderbuildstep import RenderBuildStep

from libpepper.cpp.cpprenderer import PepCppRenderer
from libpepper.environment import PepEnvironment
from libpepper import builtins

def eval_program( prog ):
    env = PepEnvironment( PepCppRenderer() )
    builtins.add_builtins( env )

    res = None
    for ln in prog:
        res = env.render_value( ln.evaluate( env ) )

    return res

def run_snippet( code ):
    return (
        eval_program(
            ParseBuildStep().process(
                LexBuildStep().process(
                    StringIO( code )
                )
            )
        )
    )

