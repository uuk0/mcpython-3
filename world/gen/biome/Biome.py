import globals as G


class BedrockType:
    DEFAULT = "enum:bedrocktype:default"
    FLAT = "enum:bedrocktype:flat"
    NONE = "enum:bedrocktype:none"


class Biome:
    FEATURE_LIST = []

    @staticmethod
    def getName():
        raise NotImplementedError()

    @staticmethod
    def getLandMassType():
        return "land"

    @staticmethod
    def getBiomeWeight():
        return 10

    @staticmethod
    def getBaseHeight():
        return 10

    @staticmethod
    def getStretchFactor():
        return 10

    @staticmethod
    def getMutationChance():
        return 30

    @staticmethod
    def getTemperature():
        return 0

    @staticmethod
    def getTopDecoratorHigh(x, z, element):
        return 5

    @staticmethod
    def getTopDecorator(x, z, lenght):
        return ["minecraft:dirt"] * (lenght - 1) + ["minecraft:grass"]

    @staticmethod
    def getDownerMaterial():
        return "minecraft:stone"

    @staticmethod
    def getBedrockType():
        return BedrockType.DEFAULT

