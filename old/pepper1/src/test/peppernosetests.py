# Copyright (C) 2011-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

import nose
from peppersamplenoseplugin import PepperSampleNosePlugin

if __name__ == '__main__':
    nose.main( addplugins = [PepperSampleNosePlugin()] )
