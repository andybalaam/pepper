# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


# Old way
from libpepper.classvalues import *
from libpepper.functionvalues import *
from libpepper.languagevalues import *
from libpepper.quotevalues import *
from libpepper.values import *

# New way - move to this
from libpepper.vals.basic_types import *
from libpepper.vals.control_flow import *
from libpepper.vals.numbers import *
from libpepper.vals.operators import *

