import globals as G
import util.noise


class IBiome:
    STRUCTURETABLE = []

    # BASIC BIOME DEFINITIONS

    @staticmethod
    def getName():
        return None

    @staticmethod
    def getTemperatur():
        return 0

    # BASIC HIGH MAP INFO

    @staticmethod
    def getBaseHigh():
        return 30

    @staticmethod
    def getBaseHighVariation():
        return 2

    @staticmethod
    def getBaseHighVariationFactor():
        return 200

    @staticmethod
    def getHighVariation():
        return 10

    @staticmethod
    def getHighFactor():
        return 200

    @staticmethod
    def getHighMapSmoothRate():
        return 4

    # BASIC BLOCKS

    @staticmethod
    def getTopDecorator():
        return "grass"

    @staticmethod
    def getDownerTopDecoration(x, y, z, dtop, dtopmax):
        return "dirt"

    @staticmethod
    def getBaseMaterial():
        return "stone"

    @staticmethod
    def getBedrockType():
        # possible: "flat", "normal", "none"
        return "normal"

    @staticmethod
    def getTopLayerRange():
        """
        :return: an list[2] of min and max of how much of the terrain height should be replaced by TopDecorators
        """
        return [4, 7]

    # BIOME MAP INFO

    @staticmethod
    def getBiomeSizeMutiplier():
        return 1

    # STRUCTURE INFO

    @staticmethod
    def getStructures():  # structure -> weight
        return {}

    @staticmethod
    def getStructurWeight():
        """how the chance is to place an structure: 1/n
        using perlin noise to select the places for"""
        return 10
