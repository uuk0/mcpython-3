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

import modloader.ModHandler

import modloader.events.LoadStageEvent

G.modhandler.search_for_mods()

import texture.TextureChanger
import texture.TextureFactory
import texture.ModelHandler

import modloader.stages.StageLoadHandler
import modloader.stages.ILoadingStage
import modloader.stages.PluginPrepareStage
import rendering.window


def main():
    window = rendering.window.Window(width=800, height=600, caption='Mcpython build '+str(G.CONFIG["BUILD"]),
                                     resizable=True)
    # Hide the mouse cursor and prevent the mouse from leaving the window.
    window.set_exclusive_mouse(True)
    setup.setup()
    G.stageloadhandler.startup()
    pyglet.app.run()


if __name__ == '__main__':
    main()
    sys.exit(0)


"""G.modhandler.post_loading_phase("startup")

import texture.TextureFactory
import texture.TextureChanger
import texture.ModelHandler
import texture.TextureAtlas
import gui.InventoryHandler
import gui.PlayerInventory
import Block.BlockHandler
import texture.BlockItemFactory
import world.gen.biome.BiomeHandler

G.modhandler.post_loading_phase("registry:init")


G.modhandler.post_loading_phase("registry:plugins")


for stage in G.modhandler.stages.values():
    stage.close()

# Load registry items


G.modhandler.post_loading_phase("registry:on_registration_begin")
G.modhandler.post_loading_phase("registry:textures:texturechangerentrys")
G.modhandler.post_loading_phase("registry:textures:texture_preparing")
G.modhandler.post_loading_phase("registry:models:load")
print("generating models")
G.modelhandler.generate()
G.modhandler.post_loading_phase("registry:textures:textureatlas:setup")
print("generating texture atlases")
G.textureatlashandler.generate()
G.modhandler.post_loading_phase("registry:inventory:load")
G.modhandler.post_loading_phase("registry:inventory:player_subitems")
G.modhandler.post_loading_phase("registry:item:load")
G.modhandler.post_loading_phase("registry:block:load")
G.modhandler.post_loading_phase("registry:biome:load")
# todo: implement here our new biome system!!!
# G.biomehandler.generate()
# world.gen.OverWorld.BIOME_SIZE *= len(G.biomehandler.biometable)
G.modhandler.post_loading_phase("registry:crafting:recipe")
G.modhandler.post_loading_phase("registry:command")

texture.BlockItemFactory.blockitemfactory.blocktable = G.blockhandler.blockarray[:]
for element in texture.BlockItemFactory.blockitemfactory.blocktable[:]:
    if not element.build_item():
        texture.BlockItemFactory.blockitemfactory.blocktable.remove(element)
texture.BlockItemFactory.blockitemfactory.maxlenght = len(texture.BlockItemFactory.blockitemfactory.blocktable)
G.modhandler.post_loading_phase("registry:block_factory_setup")


G.modhandler.post_loading_phase("load:finished")


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
"""