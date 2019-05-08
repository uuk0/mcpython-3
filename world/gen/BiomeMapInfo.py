import globals as G
import world.gen.biome.Biome
import world.gen.biome.BiomeHandler
import opensimplex
import util.biomeborder
# import noise

BIOME_SIZE = 4
MUTATED_BIOME_SIZE = 4


class BiomeMapInfo:
    def __init__(self, dimensionacccess):
        self.dimensionaccess = dimensionacccess
        self.map = {}
        self.biomenoise = None
        self.mutatedbiomenoise = None
        self.mutatedbiomenoise_2 = None
        self.mutatedbiomeselectionnoise = None
        self.generated = []
        self.bordermap = util.biomeborder.BiomeBorderGenerator()

    def generate_for_chunk(self, chunk):
        if chunk in self.generated: return
        self.bordermap.generate_for_chunk(chunk)
        self.generated.append(chunk)
        self.dimensionaccess.worldgenerationprovider.landmassinfo.generate_for_chunk(chunk)
        self.dimensionaccess.worldgenerationprovider.temperatureinfo.generate_for_chunk(chunk)
        seed = self.dimensionaccess.worldgenerationprovider.seed
        if not self.biomenoise: self.biomenoise = opensimplex.OpenSimplex(seed * 100 + 2)
        if not self.mutatedbiomenoise: self.mutatedbiomenoise = opensimplex.OpenSimplex(seed*100+20)
        if not self.mutatedbiomenoise_2: self.mutatedbiomenoise_2 = opensimplex.OpenSimplex(seed*100+40)
        if not self.mutatedbiomeselectionnoise: self.mutatedbiomeselectionnoise = opensimplex.OpenSimplex(seed*100+5)
        for x in range(chunk[0]*16, chunk[0]*16+16):
            for z in range(chunk[1]*16, chunk[1]*16+16):
                landmass = self.dimensionaccess.worldgenerationprovider.landmassinfo[(x, z)]
                if landmass in G.biomehandler.biomearrays:
                    temp = self.dimensionaccess.worldgenerationprovider.temperatureinfo[(x, z)]
                    biomearray = G.biomehandler.biomearrays[landmass]
                    biomekeys = list(biomearray.keys())
                    biomekeys.sort(key=lambda temperature: abs(temp - temperature))
                    biomearray = biomearray[biomekeys[0]]
                    value = self.biomenoise.noise3d(x/1000/BIOME_SIZE, -10, z/1000/BIOME_SIZE) * 0.5 + 0.5
                    value += self.biomenoise.noise3d(x/10000/BIOME_SIZE, -40329, -z/10000/BIOME_SIZE) * 0.5 + 0.5
                    value += self.biomenoise.noise3d(x/100000/BIOME_SIZE, seed**BIOME_SIZE,
                                                     -z/100000/BIOME_SIZE) * 0.5 + 0.5
                    value /= 3
                    value *= len(biomearray)
                    value = round(value)
                    if value >= len(biomearray): value = 0
                    biome = biomearray[value]
                    self.map[(x, z)] = biome
        for x in range(chunk[0]*16, chunk[0]*16+16):
            for z in range(chunk[1]*16, chunk[1]*16+16):
                self._mutated_helper(x, z, chunk, seed)

    def _mutated_helper(self, x, z, chunk, seed):
        biome = self.map[(x, z)]
        if biome not in G.biomehandler.biomeextra: return
        mutated_variants = G.biomehandler.biomeextra[biome]
        value = self.mutatedbiomenoise.noise3d(x / 100 / MUTATED_BIOME_SIZE,
                                               -z / 100 / MUTATED_BIOME_SIZE,
                                               seed / 100 / MUTATED_BIOME_SIZE) * 0.5 - 0.5

        value *= biome.getMutationChance()
        value = round(value)
        if value == biome.getMutationChance() // 2:
            # mutate it !!!
            selection_value = self.mutatedbiomeselectionnoise.noise3d(x/100/MUTATED_BIOME_SIZE+seed,
                                                                      -z/100/MUTATED_BIOME_SIZE-seed,
                                                                      (x * 100 - z * 10) / 10000) * 0.5 + 0.5
            selection_value *= len(mutated_variants)
            selection_value = round(selection_value)
            if selection_value >= len(mutated_variants): selection_value = 0
            mutated_biome = mutated_variants[selection_value]
            self.map[(x, z)] = mutated_biome

    def __getitem__(self, item):
        return self.map[item]

    def __setitem__(self, key, value):
        if type(key) in [list, tuple] and len(key) == 2:
            self.map[key] = value
        else:
            raise ValueError("can't set type "+str(key)+" as key. No (x, z)-vector")

