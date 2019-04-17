"""
not fully implementation of plains biome of minecraft
missing: sunflower plains, animals, ores
"""

import globals as G
import world.gen.biome.IBiome
import world.gen.structure.tree.OakTree
import world.gen.structure.OreProvider


@G.biomehandler
class Plains(world.gen.biome.IBiome.IBiome):
    @staticmethod
    def getName():
        return "minecraft:plains"

    @staticmethod
    def getStructureHeightAmount():
        return 0.2

    @staticmethod
    def getStructures():  # structure -> weight
        return [world.gen.structure.tree.OakTree.oaktreeplains,
                world.gen.structure.OreProvider.COAL_ORE,
                world.gen.structure.OreProvider.IRON_ORE,
                world.gen.structure.OreProvider.GOLD_ORE,
                world.gen.structure.OreProvider.EMERALD_ORE,
                world.gen.structure.OreProvider.REDSTONE_ORE,
                world.gen.structure.OreProvider.DIAMOND_ORE,
                world.gen.structure.OreProvider.LAPIS_ORE]

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

