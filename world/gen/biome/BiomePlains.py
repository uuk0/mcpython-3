import globals as G
import world.gen.biome.Biome
import world.gen.feature.structure.OakTree
import world.gen.feature.GrassPlant
import world.gen.feature.FlowerGenerator


@G.biomehandler
class BiomePlains(world.gen.biome.Biome.Biome):
    FEATURE_LIST = [world.gen.feature.structure.OakTree.PLAINS,
                    world.gen.feature.GrassPlant.GrassPlant(),
                    world.gen.feature.FlowerGenerator.FlowerGenerator(15, enable_tulips=True)]

    @staticmethod
    def getName():
        return "minecraft:plains"

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
        return 100

