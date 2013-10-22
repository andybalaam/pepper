# Copyright (C) 2011-2013 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

import sys

from gen import MetaPepperLexer
from gen import MetaPepperParser

lexer = MetaPepperLexer.Lexer( sys.argv[1] )

parser = MetaPepperParser.Parser( lexer )

parser.program()

