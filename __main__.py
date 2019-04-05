"""
mcpython is an minecraft clone written in python using pyglet
it is based on code of fogleman
"""

import config
import globals as G
import setup
import pyglet
import sys
import shutil
import os

if "--debug" in sys.argv:
    G.CONFIG["BUILD"] += 1
    config.store()
    import builder
    builder.build()

# Startup header

print("-------------------"+"-"*len(str(G.CONFIG["BUILD"])))
print("- mcpython build "+str(G.CONFIG["BUILD"])+" -")
print("-------------------"+"-"*len(str(G.CONFIG["BUILD"])))
print("\n"*3)


print("cleaning up tmp-dir")

if not os.path.exists(G.local+"/tmp"): os.makedirs(G.local+"/tmp")
for path in os.listdir(G.local+"/tmp"):
    if os.path.isdir(G.local+"/tmp/"+path):
        shutil.rmtree(G.local+"/tmp/"+path)
    else:
        os.remove(G.local+"/tmp/"+path)


# loading own moduls

import texture.TextureFactory
import texture.TextureChanger
import texture.ModelHandler
import texture.TextureAtlas
import gui.InventoryHandler
import gui.PlayerInventory
import Block.BlockHandler
import world.gen.biome.BiomeHandler
import rendering.window


# Setup all handlers

print("generating models")
G.modelhandler.generate()

print("generating texture atlases")
G.textureatlashandler.generate()


# Starting game


def main():
    window = rendering.window.Window(width=800, height=600, caption='Mcpython build '+str(G.CONFIG["BUILD"]),
                                     resizable=True)
    # Hide the mouse cursor and prevent the mouse from leaving the window.
    window.set_exclusive_mouse(True)
    setup.setup()
    pyglet.app.run()


if __name__ == '__main__':
    main()
