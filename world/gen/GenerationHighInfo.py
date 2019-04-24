import globals as G
import opensimplex
import math
import util.vector


class GenerationHighInfo:
    def __init__(self, dimensionacccess):
        self.dimensionaccess = dimensionacccess
        self.basenoise = None
        self.map = {}  # (x, z) -> (from, to, toplayerhigh)[].sort(key=lamda x: x[1])
        self.generated = []
        self.basehighraw = {}

    def generate_for_chunk(self, chunk):
        if chunk in self.generated: return
        self.generated.append(chunk)
        if not self.basenoise:
            self.basenoise = opensimplex.OpenSimplex(self.dimensionaccess.worldgenerationprovider.seed*100+3)
        for x in range(chunk[0]*16, chunk[0]*16+16):
            for z in range(chunk[1]*16, chunk[1]*16+16):
                biome = self.dimensionaccess.worldgenerationprovider.biomemap[(x, z)]
                max_high = self._get_base_high_smooth(x, z)
                data = [(0, max_high, max_high-biome.getTopDecoratorHigh(x, z, 0))]

                data.sort(key=lambda x: x[1])
                self.map[(x, z)] = data

    def _get_base_high(self, x, z):
        if (x, z) not in self.dimensionaccess.worldgenerationprovider.biomemap.map:
            self.dimensionaccess.worldgenerationprovider.biomemap.generate_for_chunk(util.vector.sectorize((x, 0, z)))
        if (x, z) in self.basehighraw: return self.basehighraw[(x, z)]
        max_high_factor = self.basenoise.noise3d(x/60, -80, z/60) / 2 + 0.5
        max_high_factor_2 = self.basenoise.noise3d(x/100, 12314702, -z/100) / 2 + 0.5
        max_high_factor_3 = self.basenoise.noise4d(x/10, z/100, x/100, z/10) / 2 + 0.5
        value = (max_high_factor + max_high_factor_2 + max_high_factor_3) / 3
        biome = self.dimensionaccess.worldgenerationprovider.biomemap[(x, z)]
        max_high = value * biome.getStretchFactor() + biome.getBaseHeight()
        self.basehighraw[(x, z)] = max_high
        return max_high

    def _get_base_high_smooth(self, x, z):
        s = []
        MAX_VALUE = 12
        for dx in range(-3, 4):
            for dz in range(-3, 4):
                if dx == dz == 0:
                    s += [self._get_base_high(x, z)] * MAX_VALUE
                else:
                    s += [self._get_base_high(x+dx, z+dz)] * round(1 / (abs(dx) + abs(dz)) * MAX_VALUE)
        return round(sum(s) / len(s))

    def __getitem__(self, item):
        return self.map[item]

    def __setitem__(self, key, value):
        if type(key) in [list, tuple] and len(key) == 2:
            self.map[key] = value
        else:
            raise ValueError("can't set type "+str(key)+" as key. No (x, z)-vector")

