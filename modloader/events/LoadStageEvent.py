import globals as G
import modloader.events.ILoadStageEvent
import modloader.stages.PluginPrepareStage
import modloader.stages.RegistrationStage
import modloader.stages.McInternLoadingStage
import modloader.stages.FinishingUpStage


registry_plugin = modloader.events.ILoadStageEvent.ILoadStageEvent("register registry plugins",
                                                                   modloader.stages.PluginPrepareStage.mainstage)

texture_setup = modloader.events.ILoadStageEvent.ILoadStageEvent("work on textures",
                                                                 modloader.stages.RegistrationStage.mainstage)

texture_changer = modloader.events.ILoadStageEvent.ILoadStageEvent("register model helpers",
                                                                   modloader.stages.RegistrationStage.mainstage)


model_load = modloader.events.ILoadStageEvent.ILoadStageEvent("register models",
                                                              modloader.stages.RegistrationStage.mainstage)


textureatlas_load = modloader.events.ILoadStageEvent.ILoadStageEvent("generating texture atlases",
                                                                     modloader.stages.RegistrationStage.mainstage)

inventory_load = modloader.events.ILoadStageEvent.ILoadStageEvent("register inventorys",
                                                                  modloader.stages.RegistrationStage.mainstage)

playerinventory_load = modloader.events.ILoadStageEvent.ILoadStageEvent("register player inventory parts",
                                                                        modloader.stages.RegistrationStage.mainstage)

items = modloader.events.ILoadStageEvent.ILoadStageEvent("register items",
                                                         modloader.stages.RegistrationStage.mainstage)

blocks = modloader.events.ILoadStageEvent.ILoadStageEvent("register blocks",
                                                          modloader.stages.RegistrationStage.mainstage)

biomes = modloader.events.ILoadStageEvent.ILoadStageEvent("register biomes",
                                                          modloader.stages.RegistrationStage.mainstage)

crafting_recipes = modloader.events.ILoadStageEvent.ILoadStageEvent("register crafting recipes",
                                                                    modloader.stages.RegistrationStage.mainstage)

commands = modloader.events.ILoadStageEvent.ILoadStageEvent("register commands",
                                                            modloader.stages.RegistrationStage.mainstage)

blockitemfactory = modloader.events.ILoadStageEvent.ILoadStageEvent("creating items for blocks",
                                                                    modloader.stages.McInternLoadingStage.mainstage)

load_finished = modloader.events.ILoadStageEvent.ILoadStageEvent("creating items for blocks",
                                                                 modloader.stages.FinishingUpStage.mainstage)

texture_atlas_generate = modloader.events.ILoadStageEvent.ILoadStageEvent("creating texture atlases",
                                                                          modloader.stages.FinishingUpStage.mainstage)


@texture_atlas_generate("minecraft", action="generating texture atlases")
def on_texture_atlas_generate(*args):
    G.textureatlashandler.generate()


model_generate = modloader.events.ILoadStageEvent.ILoadStageEvent("creating models",
                                                                  modloader.stages.FinishingUpStage.mainstage)


@model_generate("minecraft", action="generating texture atlases")
def on_model_generate(*args):
    G.modelhandler.generate()


stages = [registry_plugin, texture_setup, texture_changer, model_load, textureatlas_load, inventory_load,
          playerinventory_load, items, blocks, biomes, crafting_recipes, commands, texture_atlas_generate,
          model_generate, blockitemfactory]


for stage in stages:
    G.modhandler.register(stage)

"""
startup = modloader.events.ILoadStageEvent.ILoadStageEvent("startup")
registryinit = modloader.events.ILoadStageEvent.ILoadStageEvent("registry:init")
registryplugins = modloader.events.ILoadStageEvent.ILoadStageEvent("registry:plugins")


# registrating phases

registry_startup = modloader.events.ILoadStageEvent.ILoadStageEvent("registry:on_registration_begin")

blockitemfactory = modloader.events.ILoadStageEvent.ILoadStageEvent("registry:block_factory_setup")

# runtime phases

worldgen_on_chunk_gen_start = modloader.events.ILoadStageEvent.ILoadStageEvent("generation:chunk:start")

worldgen_on_chunk_gen_end = modloader.events.ILoadStageEvent.ILoadStageEvent("generation:chunk:end")


load_finished = modloader.events.ILoadStageEvent.ILoadStageEvent("load:finished")
"""
