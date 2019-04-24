import world.gen.feature.IFeature
import util.vector


class DeadBushGenerator(world.gen.feature.IFeature.IFeature):
    def __init__(self, size):
        self.size = size

    def get_possible_y_coordinates_for(self, x, z, worldgenerationprovider):
        high = worldgenerationprovider.highmap[(x, z)][-1][1]+1
        chunk = util.vector.sectorize((x, 0, z))
        if (x, high, z) in worldgenerationprovider.dimensionaccess.get_chunk_for(chunk, generate=False).world:
            return []
        return [high]

    def generate(self, x, y, z, worldgenerationprovider):
        worldgenerationprovider.dimensionaccess.add_block((x, y, z), "minecraft:dead_bush")

    def get_paste_tries(self):
        return self.size * 10

    def get_properility(self):
        return 2

