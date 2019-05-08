import globals as G
import world.gen.biome.BiomeMountains
import world.gen.feature.OreProvider
import world.gen.feature.GrassPlant
import world.gen.feature.structure.OakTree
import world.gen.feature.SnowLayer
import world.gen.feature.structure.SpruceTree


class BiomeWoddedMountains(world.gen.biome.BiomeMountains.Mountains):
    FEATURE_LIST = [world.gen.feature.GrassPlant.GrassPlant(), world.gen.feature.OreProvider.EMERALD,
                    world.gen.feature.SnowLayer.SnowLayer(30),
                    world.gen.feature.structure.SpruceTree.SpruceTree(20, 2)] + \
                    world.gen.feature.OreProvider.DEFAULT_ORE_PROVIDER.get_ores() + \
                    world.gen.feature.OreProvider.DEFAULT_STONE_PROVIDER.get_ores()

    @staticmethod
    def getName():
        return "minecraft:wooded_mountains"


G.biomehandler(BiomeWoddedMountains, world.gen.biome.BiomeMountains.Mountains.getName())

