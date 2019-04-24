import globals as G
import world.gen.feature.IFeature
import random
import opensimplex
import util.vector

DEFAULT_FLOWERS = ["minecraft:dandelion", "minecraft:allium", "minecraft:azure_bluet", "minecraft:cornflower",
                   "minecraft:lily_of_the_valley", "minecraft:blue_orchid", "minecraft:oxeye_daisy", "minecraft:poppy",
                   "minecraft:lilac", "minecraft:peony", "minecraft:rose_bush"]

EXTRA_TULPIS = ["minecraft:orange_tulip", "minecraft:pink_tulip", "minecraft:red_tulip", "minecraft:white_tulip"]

orchid_noise = opensimplex.OpenSimplex(G.CONFIG["seed"])


class FlowerGenerator(world.gen.feature.IFeature.IFeature):
    def __init__(self, size, enable_tulips=False, tulip_chance=5):
        self.size = size
        self.enable_orchids = enable_tulips
        self.orchid_chance = tulip_chance

    def get_possible_y_coordinates_for(self, x, z, worldgenerationprovider):
        high = worldgenerationprovider.highmap[(x, z)][-1][1]+1
        chunk = util.vector.sectorize((x, 0, z))
        if (x, high, z) in worldgenerationprovider.dimensionaccess.get_chunk_for(chunk, generate=False).world:
            return []
        return [high]

    def generate(self, x, y, z, worldgenerationprovider):
        if self.enable_orchids and round(orchid_noise.noise2d(x, z) * self.orchid_chance) == 1 and len(EXTRA_TULPIS) > 0:
            worldgenerationprovider.dimensionaccess.add_block((x, y, z), random.choice(EXTRA_TULPIS))
        else:
            worldgenerationprovider.dimensionaccess.add_block((x, y, z), random.choice(DEFAULT_FLOWERS))

    def get_paste_tries(self):
        return self.size * 10

    def get_properility(self):
        return 2

