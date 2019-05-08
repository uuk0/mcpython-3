import globals as G
import world.gen.biome.Biome
import world.gen.feature.structure.OakTree
import world.gen.biome.BiomePlains
import world.gen.feature.GrassPlant
import world.gen.feature.FlowerGenerator


class BiomeSunflowerPlains(world.gen.biome.Biome.Biome):
    FEATURE_LIST = [world.gen.feature.GrassPlant.GrassPlant(),
                    world.gen.feature.FlowerGenerator.FlowerGenerator(10)]

    @staticmethod
    def getName():
        return "minecraft:sunflower_plains"

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
    def getTemperature():
        return 0.8


G.biomehandler.register(BiomeSunflowerPlains, super_biome=world.gen.biome.BiomePlains.BiomePlains)

