import globals as G
import world.gen.biome.Biome
import world.gen.feature.OreProvider
import world.gen.feature.GrassPlant
import world.gen.feature.structure.OakTree
import world.gen.feature.SnowLayer


@G.biomehandler
class Mountains(world.gen.biome.Biome.Biome):
    FEATURE_LIST = [world.gen.feature.GrassPlant.GrassPlant(), world.gen.feature.OreProvider.EMERALD,
                    world.gen.feature.SnowLayer.SnowLayer(30)] + \
        world.gen.feature.OreProvider.DEFAULT_ORE_PROVIDER.get_ores() + \
        world.gen.feature.OreProvider.DEFAULT_STONE_PROVIDER.get_ores()

    @staticmethod
    def getName():
        return "minecraft:mountains"

    @staticmethod
    def getBiomeWeight():
        return 10

    @staticmethod
    def getBaseHeight():
        return 65

    @staticmethod
    def getStretchFactor():
        return 100

    @staticmethod
    def getMutationChance():
        return 30

    @staticmethod
    def getTemperature():
        return 0.2

