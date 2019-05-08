import globals as G
import world.gen.biome.BiomeMountains
import world.gen.biome.Biome
import world.gen.feature.OreProvider
import world.gen.feature.GrassPlant
import world.gen.feature.structure.OakTree
import world.gen.feature.SnowLayer


class BiomeGravellyMountains(world.gen.biome.BiomeMountains.Mountains):
    FEATURE_LIST = [world.gen.feature.GrassPlant.GrassPlant(), world.gen.feature.OreProvider.EMERALD] + \
                    world.gen.feature.OreProvider.DEFAULT_ORE_PROVIDER.get_ores() + \
                    world.gen.feature.OreProvider.DEFAULT_STONE_PROVIDER.get_ores()

    @staticmethod
    def getTopDecorator(x, z, lenght):
        return ["minecraft:gravel"] * lenght

    @staticmethod
    def getName():
        return "minecraft:gravelly_mountains"


G.biomehandler(BiomeGravellyMountains, world.gen.biome.BiomeMountains.Mountains.getName())

