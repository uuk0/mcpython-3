import globals as G
import world.gen.biome.Biome
import world.gen.biome.BiomeHandler
import opensimplex

BIOME_SIZE = 4


class BiomeMapInfo:
    def __init__(self, dimensionacccess):
        self.dimensionaccess = dimensionacccess
        self.map = {}
        self.biomenoise = None
        self.generated = []

    def generate_for_chunk(self, chunk):
        if chunk in self.generated: return
        self.generated.append(chunk)
        self.dimensionaccess.worldgenerationprovider.landmassinfo.generate_for_chunk(chunk)
        self.dimensionaccess.worldgenerationprovider.temperatureinfo.generate_for_chunk(chunk)
        if not self.biomenoise:
            self.biomenoise = opensimplex.OpenSimplex(self.dimensionaccess.worldgenerationprovider.seed * 100 + 2)
        for x in range(chunk[0]*16, chunk[0]*16+16):
            for z in range(chunk[1]*16, chunk[1]*16+16):
                landmass = self.dimensionaccess.worldgenerationprovider.landmassinfo[(x, z)]
                if landmass in G.biomehandler.biomearrays:
                    temp = self.dimensionaccess.worldgenerationprovider.temperatureinfo[(x, z)]
                    biomearray = G.biomehandler.biomearrays[landmass]
                    biomekeys = list(biomearray.keys())
                    biomekeys.sort(key=lambda temperature: abs(temp - temperature))
                    biomearray = biomearray[biomekeys[0]]
                    value = self.biomenoise.noise3d(x/100/BIOME_SIZE, -10, z/100/BIOME_SIZE) * 0.5 + 0.5
                    value += self.biomenoise.noise3d(x/1000/BIOME_SIZE, -40329, -z/1000/BIOME_SIZE) * 0.5 + 0.5
                    value /= 2
                    value *= len(biomearray)
                    value = round(value)
                    if value >= len(biomearray): value = 0
                    biome = biomearray[value]
                    rvalue = self.biomenoise.noise3d(x/10, biome.getBiomeWeight(), z/10) * biome.getMutationChance()
                    if (round(rvalue) == 0 or round(rvalue) == biome.getMutationChance()) and \
                            biome in G.biomehandler.biomeextra:
                        mutationarray = G.biomehandler.biomeextra[biome]
                        mutationvalue = round(self.biomenoise.noise3d(x/10/BIOME_SIZE, -10, z/10/BIOME_SIZE)
                                              * len(mutationarray))
                        if mutationvalue >= len(mutationarray): mutationvalue = 0
                        mutatedbiome = mutationarray[mutationvalue]
                        self.map[(x, z)] = mutatedbiome
                    else:
                        self.map[(x, z)] = biome

    def __getitem__(self, item):
        return self.map[item]

    def __setitem__(self, key, value):
        if type(key) in [list, tuple] and len(key) == 2:
            self.map[key] = value
        else:
            raise ValueError("can't set type "+str(key)+" as key. No (x, z)-vector")

