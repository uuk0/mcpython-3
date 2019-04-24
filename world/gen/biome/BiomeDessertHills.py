import world.gen.biome.BiomeDessert
import globals as G


class BiomeDessertHills(world.gen.biome.BiomeDessert.BiomeDessert):
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

