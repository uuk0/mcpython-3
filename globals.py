"""
main file for all things that every part of the program should remember
"""

import sys, os

local = os.path.dirname(sys.argv[0])


CONFIG = {}

model = None

window = None


blockhandler = None

itemhandler = None


textureatlashandler = None

modelhandler = None

biomehandler = None

texturechangerhandler = None

inventoryhandler = None

