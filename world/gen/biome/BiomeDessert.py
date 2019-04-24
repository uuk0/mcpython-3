import globals as G
import world.gen.biome.Biome
import world.gen.feature.dead_bush
import world.gen.feature.SugarCaneGenerator


@G.biomehandler
class BiomeDessert(world.gen.biome.Biome.Biome):
    FEATURE_LIST = [world.gen.feature.dead_bush.DeadBushGenerator(2),
                    world.gen.feature.SugarCaneGenerator.SugarCaneGenerator(0.5)]

    @staticmethod
    def getName():
        return "minecraft:dessert"

    @staticmethod
    def getLandMassType():
        return "land"

    @staticmethod
    def getBaseHeight():
        return 50

    @staticmethod
    def getStretchFactor():
        return 30

    @staticmethod
    def getMutationChance():
        return 30

    @staticmethod
    def getTopDecoratorHigh(x, z, element):
        return 12

    @staticmethod
    def getTopDecorator(x, z, lenght):
        return ["minecraft:sandstone"] * (lenght - 8) + ["minecraft:sand"] * 8

    @staticmethod
    def getBiomeWeight():
        return 10

