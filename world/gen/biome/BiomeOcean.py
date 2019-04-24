import globals as G
import world.gen.biome.Biome

#todo: remove


@G.biomehandler
class BiomeOcean(world.gen.biome.Biome.Biome):
    @staticmethod
    def getName():
        return "minecraft:ocean"

    @staticmethod
    def getLandMassType():
        return "ocean"

    @staticmethod
    def getMutationChance():
        return 1

    @staticmethod
    def getTopDecorator(x, z, lenght):
        return ["minecraft:gravel"] * lenght

