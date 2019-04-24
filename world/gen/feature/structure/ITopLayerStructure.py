import globals as G
import world.gen.feature.IFeature


class ITopLayerStructure(world.gen.feature.IFeature.IFeature):
    def get_possible_y_coordinates_for(self, x, z, worldgenerationprovider):
        return [worldgenerationprovider.highmap[(x, z)][-1][1]+1]

    def generate(self, x, y, z, worldgenerationprovider):
        raise NotImplementedError()

