import globals as G
import opensimplex


class LandMassInfo:
    # todo: specifie for every dimension
    def __init__(self, dimensionaccess):
        self.landmassnoise = None
        self.map = {}
        self.landmasstypes = [("land", 7), ("ocean", 2)]
        self.table = []
        self.dimensionaccess = dimensionaccess
        self.generated = []

    def generate_table(self):
        for element in self.landmasstypes:
            self.table += [element[0]] * element[1]

    def generate_for_chunk(self, chunk):
        if chunk in self.generated: return
        self.generated.append(chunk)
        if not self.landmassnoise:
            self.landmassnoise = opensimplex.OpenSimplex(self.dimensionaccess.worldgenerationprovider.seed * 100)
        for x in range(chunk[0]*16, chunk[0]*16+16):
            for z in range(chunk[1]*16, chunk[1]*16+16):
                self._select_type(x, z)

    def _select_type(self, x, z):
        if not self.table: self.generate_table()
        value1 = self.landmassnoise.noise4d(x/100+10, 10, z/100-20, -100) / 2 + 0.5
        value2 = self.landmassnoise.noise4d(round(x/100-10), 100, round(z/100+20), 100) / 2 + 0.5
        values = [value1] * 100 + [value2]
        value = sum(values) / len(values)
        value *= len(self.table)
        value = round(value)
        if value >= len(self.table): value = 0
        # print(value, x, z, self.table[value])
        key = self.table[value]
        self.map[(x, z)] = key

    def __getitem__(self, item):
        return self.map[item]

    def __setitem__(self, key, value):
        if type(key) in [list, tuple] and len(key) == 2:
            self.map[key] = value
        else:
            raise ValueError("can't set type "+str(key)+" as key. No (x, z)-vector")

