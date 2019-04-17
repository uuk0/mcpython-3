import globals as G
import world.gen.biome.IBiome
import util.noise


@G.biomehandler
class Dessert(world.gen.biome.IBiome.IBiome):
    @staticmethod
    def getStructureHeightAmount():
        return 0.2

    @staticmethod
    def getStructures():  # structure -> weight
        return [world.gen.structure.OreProvider.COAL_ORE,
                world.gen.structure.OreProvider.IRON_ORE,
                world.gen.structure.OreProvider.GOLD_ORE,
                world.gen.structure.OreProvider.EMERALD_ORE,
                world.gen.structure.OreProvider.REDSTONE_ORE,
                world.gen.structure.OreProvider.DIAMOND_ORE,
                world.gen.structure.OreProvider.LAPIS_ORE]

    @staticmethod
    def getName():
        return "minecraft:dessert"

    @staticmethod
    def getTemperatur():
        return 2

    @staticmethod
    def getTopDecorator():
        return "sand"

    @staticmethod
    def getDownerTopDecoration(x, y, z, dtop, dtopmax):
        return "sand" if util.noise.noise(x, y, z, dtop*dtopmax) * dtopmax / 2 + dtopmax / 2 > dtop + 3  else "sandstone"

    @staticmethod
    def getBaseMaterial():
        return "stone"

    @staticmethod
    def getTopLayerRange():
        return [7, 12]

    @staticmethod
    def getBiomeSizeMutiplier():
        return 1 # 4


@G.biomehandler
class DessertHills(Dessert):
    @staticmethod
    def getBaseHigh():
        return 40

    @staticmethod
    def getBaseHighVariation():
        return 4

    @staticmethod
    def getBaseHighVariationFactor():
        return 100

    @staticmethod
    def getHighVariation():
        return 20

    @staticmethod
    def getHighFactor():
        return 30

    @staticmethod
    def getHighMapSmoothRate():
        return 3

