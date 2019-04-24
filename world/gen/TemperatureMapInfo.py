import globals as G
import opensimplex


class TemperatureMapInfo:
    def __init__(self, dimensionaccess):
        self.dimensionaccess = dimensionaccess
        self.temperaturmapsnoise = None
        self.map = {}
        self.generated = []

    def generate_for_chunk(self, chunk):
        if chunk in self.generated: return
        self.generated.append(chunk)
        if not self.temperaturmapsnoise:
            self.temperaturmapsnoise = opensimplex.OpenSimplex(
                self.dimensionaccess.worldgenerationprovider.seed * 100 + 1)
        for x in range(chunk[0]*16, chunk[0]*16+16):
            for z in range(chunk[1]*16, chunk[1]*16+16):
                self.map[(x, z)] = self.temperaturmapsnoise.noise3d(x/100, z/100, -10) * 2

    def __getitem__(self, item):
        return self.map[item]

    def __setitem__(self, key, value):
        if type(key) in [list, tuple] and len(key) == 2:
            self.map[key] = value
        else:
            raise ValueError("can't set type "+str(key)+" as key. No (x, z)-vector")



