import globals as G


class IFeature:
    def generate(self, x, y, z, worldgenerationprovider):
        raise NotImplementedError()

    def get_possible_y_coordinates_for(self, x, z, worldgenerationprovider):
        return []

    def get_paste_tries(self):
        return 0

    def get_properility(self):
        return 1

