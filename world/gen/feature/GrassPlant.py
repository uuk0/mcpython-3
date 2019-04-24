import globals as G
import world.gen.feature.IFeature
import random


class GrassPlant(world.gen.feature.IFeature.IFeature):
    def get_possible_y_coordinates_for(self, x, z, worldgenerationprovider):
        return [worldgenerationprovider.highmap[(x, z)][-1][1]+1]

    def generate(self, x, y, z, worldgenerationprovider):
        if random.randint(1, 8) == 1:
            worldgenerationprovider.dimensionaccess.add_block((x, y, z), "minecraft:tall_grass")
        else:
            worldgenerationprovider.dimensionaccess.add_block((x, y, z), "minecraft:grass_small")

    def get_paste_tries(self):
        return 80

    def get_properility(self):
        return 2

