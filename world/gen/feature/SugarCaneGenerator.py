import world.gen.feature.IFeature
import util.vector
import random


class SugarCaneGenerator(world.gen.feature.IFeature.IFeature):
    def __init__(self, size):
        self.size = size

    def get_possible_y_coordinates_for(self, x, z, worldgenerationprovider):
        high = worldgenerationprovider.highmap[(x, z)][-1][1]+1
        chunk = util.vector.sectorize((x, 0, z))
        if (x, high, z) in worldgenerationprovider.dimensionaccess.get_chunk_for(chunk, generate=False).world:
            return []
        return [high]

    def generate(self, x, y, z, worldgenerationprovider):
        height = random.randint(1, 3)
        for dy in range(height):
            worldgenerationprovider.dimensionaccess.add_block((x, y+dy, z), "minecraft:sugar_cane")

    def get_paste_tries(self):
        return round(self.size * 10)

    def get_properility(self):
        return 2

