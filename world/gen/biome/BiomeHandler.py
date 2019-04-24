import globals as G
import world.gen.biome.Biome
import modloader.events.LoadStageEvent


class BiomeHandler:
    def __init__(self):
        self.biomes = {}
        self.biomearrays = {}
        self.biomeextra = {}

    def __call__(self, biome: world.gen.biome.Biome.Biome, super_biome=None):
        self.biomes[biome.getName()] = biome
        if not super_biome:
            if not biome.getLandMassType() in self.biomearrays: self.biomearrays[biome.getLandMassType()] = {}
            if not biome.getTemperature() in self.biomearrays[biome.getLandMassType()]:
                self.biomearrays[biome.getLandMassType()][biome.getTemperature()] = []
            self.biomearrays[biome.getLandMassType()][biome.getTemperature()] += [biome] * biome.getBiomeWeight()
        else:
            if type(super_biome) == str:
                super_biome = self.biomes[super_biome]
            if super_biome not in self.biomeextra: self.biomeextra[super_biome] = []
            self.biomeextra[super_biome] += [biome] * biome.getBiomeWeight()
        return biome

    def register(self, *args, **kwargs):
        self(*args, **kwargs)


G.biomehandler = BiomeHandler()


@modloader.events.LoadStageEvent.biomes("minecraft")
def load_biomes(eventname):
    # land mask: ocean
    from world.gen.biome import (BiomeOcean)

    # land mask: land
    from world.gen.biome import (BiomePlains, BiomeSunflowerPlains, BiomeDessert, BiomeDessertHills)

