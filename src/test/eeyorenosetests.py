import nose
from eeyoresamplenoseplugin import EeyoreSampleNosePlugin

if __name__ == '__main__':
    nose.main( addplugins = [EeyoreSampleNosePlugin()] )
