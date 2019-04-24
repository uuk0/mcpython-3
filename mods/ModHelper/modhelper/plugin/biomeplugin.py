import globals as G
import world.gen.biome.IBiome
import modloader.events.LoadStageEvent
import modloader.events.ILoadStageEvent


biomeplugin = modloader.events.ILoadStageEvent.ILoadStageEvent("modhelper:plugins:biome")


@modloader.events.LoadStageEvent.biomes
def load_plugins():
    G.modhandler.post_loading_phase("modhelper:plugins:biome")


class BiomePluginHandler:
    def __init__(self):
        self.plugins = []
        self.modified = []

    def add(self, plugin):
        mods = plugin.get_modified_chunks()
        for mod in mods:
            if any([mod[0] == x[0] for x in self.modified]):
                if mod[1] in ["all"]:
                    return
        self.plugins.append(plugin)
        self.modified += plugin.get_modified_chunks()

    def apply(self):
        for plugin in self.plugins:
            plugin.apply()


biomepluginhandler = BiomePluginHandler()


class IBiomePlugin:
    def apply(self):
        raise NotImplementedError()

    def get_modified_chunks(self):
        return []


class OverWrite(IBiomePlugin):
    def __init__(self, biome_name_list_or_biome_name, biome_overwrite):
        self.biomes = biome_name_list_or_biome_name if type(biome_name_list_or_biome_name) in \
                                                       (list, tuple, set) else [biome_name_list_or_biome_name]

    def apply(self):
        pass

    def get_modified_chunks(self):
        return [(x, "all") for x in self.biomes]



