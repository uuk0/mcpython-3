import globals as G
import world.gen.biome.Biome
import world.gen.feature.OreProvider

#todo: remove


@G.biomehandler
class BiomeOcean(world.gen.biome.Biome.Biome):
    FEATURE_LIST = world.gen.feature.OreProvider.DEFAULT_ORE_PROVIDER.get_ores() + \
                   world.gen.feature.OreProvider.DEFAULT_STONE_PROVIDER.get_ores()

    @staticmethod
    def getName():
        return "minecraft:ocean"

    @staticmethod
    def getLandMassType():
        return "ocean"

    @staticmethod
    def getMutationChance():
        return 1

    @staticmethod
    def getTopDecorator(x, z, lenght):
        return ["minecraft:gravel"] * lenght

