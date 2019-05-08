import world.gen.biome.BiomeDessert
import globals as G
import world.gen.feature.OreProvider


class BiomeDessertHills(world.gen.biome.BiomeDessert.BiomeDessert):
    FEATURE_LIST = world.gen.feature.OreProvider.DEFAULT_ORE_PROVIDER.get_ores() + \
                    world.gen.feature.OreProvider.DEFAULT_STONE_PROVIDER.get_ores()

    @staticmethod
    def getStretchFactor():
        return 40

    @staticmethod
    def getBaseHeight():
        return 60

    @staticmethod
    def getName():
        return "minecraft:dessert_hills"


G.biomehandler(BiomeDessertHills, "minecraft:dessert")

