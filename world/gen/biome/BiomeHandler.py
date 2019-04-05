import globals as G
import world.gen.OverWorld


class BiomeHandler:
    def __init__(self):
        self.biomes = {}
        self.biometable = []

    def __call__(self, *args, **kwargs):
        self.biomes[args[0].getName()] = args[0]

        return args[0]

    def generate(self):
        biomes = list(self.biomes.values())
        biomes.sort(key=lambda x: x.getTemperatur())
        for biome in biomes:
            self.biometable += [biome] * biome.getBiomeSizeMutiplier()

    def register(self, biome):
        self(biome)


G.biomehandler = BiomeHandler()


from . import Ocean, Plains, Dessert


G.biomehandler.generate()


world.gen.OverWorld.BIOME_SIZE *= len(G.biomehandler.biometable)

