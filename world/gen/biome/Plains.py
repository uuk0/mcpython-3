"""
not fully implementation of plains biome of minecraft
missing: sunflower plains, animals, ores
"""

import globals as G
import world.gen.biome.IBiome
import world.gen.structure.tree.OakTree


@G.biomehandler
class Plains(world.gen.biome.IBiome.IBiome):
    @staticmethod
    def getName():
        return "minecraft:plains"

    @staticmethod
    def getStructures():  # structure -> weight
        return {world.gen.structure.tree.OakTree.oaktree: 1}

    @staticmethod
    def getStructurWeight():
        return 200000

    @staticmethod
    def getBaseHighVariation():
        return 1

    @staticmethod
    def getBaseHighVariationFactor():
        return 400

    @staticmethod
    def getHighVariation():
        return 5

    @staticmethod
    def getTemperatur():
        return 0.8


@G.biomehandler
class SunflowerPlains(Plains):
    """
    todo: implement this
    """

    @staticmethod
    def getName():
        return "minecraft:sunflower_plains"

