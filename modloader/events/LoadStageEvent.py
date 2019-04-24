import globals as G
import modloader.events.ILoadStageEvent


startup = modloader.events.ILoadStageEvent.ILoadStageEvent("startup")
registryinit = modloader.events.ILoadStageEvent.ILoadStageEvent("registry:init")
registryplugins = modloader.events.ILoadStageEvent.ILoadStageEvent("registry:plugins")


# registrating phases

registry_startup = modloader.events.ILoadStageEvent.ILoadStageEvent("registry:on_registration_begin")
texture_setup = modloader.events.ILoadStageEvent.ILoadStageEvent("registry:textures:texture_preparing")
texture_changer = modloader.events.ILoadStageEvent.ILoadStageEvent("registry:textures:texturechangerentrys")
model_load = modloader.events.ILoadStageEvent.ILoadStageEvent("registry:models:load")
textureatlas_load = modloader.events.ILoadStageEvent.ILoadStageEvent("registry:textures:textureatlas:setup")
inventory_load = modloader.events.ILoadStageEvent.ILoadStageEvent("registry:inventory:load")
playerinventory_load = modloader.events.ILoadStageEvent.ILoadStageEvent("registry:inventory:player_subitems")
items = modloader.events.ILoadStageEvent.ILoadStageEvent("registry:item:load")
blocks = modloader.events.ILoadStageEvent.ILoadStageEvent("registry:block:load")
biomes = modloader.events.ILoadStageEvent.ILoadStageEvent("registry:biome:load")
crafting_recipes = modloader.events.ILoadStageEvent.ILoadStageEvent("registry:crafting:recipe")
commands = modloader.events.ILoadStageEvent.ILoadStageEvent("registry:command")
blockitemfactory = modloader.events.ILoadStageEvent.ILoadStageEvent("registry:block_factory_setup")

# runtime phases

worldgen_prepare = modloader.events.ILoadStageEvent.ILoadStageEvent("worldgen:prepare")
worldgen_start = modloader.events.ILoadStageEvent.ILoadStageEvent("worldgen:start")
worldgen_end = modloader.events.ILoadStageEvent.ILoadStageEvent("worldgen:end")


load_finished = modloader.events.ILoadStageEvent.ILoadStageEvent("load:finished")


stages = [startup, registryinit, registryplugins,
          registry_startup, texture_setup, texture_changer, model_load, textureatlas_load, inventory_load,
          playerinventory_load, items, blocks, biomes, crafting_recipes, commands, blockitemfactory,
          worldgen_prepare, worldgen_start, worldgen_end, load_finished]


for stage in stages:
    G.modhandler.register(stage)

