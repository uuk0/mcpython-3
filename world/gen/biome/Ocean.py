"""
not fully implementation of ocean biome of minecraft
"""

import globals as G
import world.gen.biome.IBiome


@G.biomehandler
class Ocean(world.gen.biome.IBiome.IBiome):
    @staticmethod
    def getName():
        return "minecraft:ocean"

    @staticmethod
    def getTopDecorator():
        return "gravel"

    @staticmethod
    def getDownerTopDecoration():
        return "gravel"

    @staticmethod
    def getBaseMaterial():
        return "stone"

    @staticmethod
    def getTopLayerRange():
        return [6, 10]

    @staticmethod
    def getBiomeSizeMutiplier():
        return 0

