import world.gen.GenerationHighInfo
import world.gen.LandMassInfo
import world.gen.TemperatureMapInfo
import world.gen.BiomeMapInfo
import globals as G
import random
import world.gen.feature.IFeature
import util.vector


class WorldGenerationProvider:
    def __init__(self, dimensionprovider, seed=G.CONFIG["seed"]):
        self.landmassinfo = world.gen.LandMassInfo.LandMassInfo(dimensionprovider)
        self.temperatureinfo = world.gen.TemperatureMapInfo.TemperatureMapInfo(dimensionprovider)
        self.biomemap = world.gen.BiomeMapInfo.BiomeMapInfo(dimensionprovider)
        self.highmap = world.gen.GenerationHighInfo.GenerationHighInfo(dimensionprovider)
        self.seed = seed
        self.dimensionaccess = dimensionprovider

    def generate_chunk(self, chunk):
        print("generating chunk", chunk)
        G.window.set_caption('Mcpython build ' + str(G.CONFIG["BUILD"]) + " | world generation | "+str(chunk) +
                             " | landmass")
        self.landmassinfo.generate_for_chunk(chunk)
        G.window.set_caption('Mcpython build ' + str(G.CONFIG["BUILD"]) + " | world generation | " + str(chunk) +
                             " | temperature map")
        self.temperatureinfo.generate_for_chunk(chunk)
        G.window.set_caption('Mcpython build ' + str(G.CONFIG["BUILD"]) + " | world generation | " + str(chunk) +
                             " | biome map")
        self.biomemap.generate_for_chunk(chunk)
        G.window.set_caption('Mcpython build ' + str(G.CONFIG["BUILD"]) + " | world generation | " + str(chunk) +
                             " | highmap")
        self.highmap.generate_for_chunk(chunk)
        G.window.set_caption('Mcpython build ' + str(G.CONFIG["BUILD"]) + " | world generation | " + str(chunk) +
                             " | adding blocks")
        for x in range(chunk[0]*16, chunk[0]*16+16):
            for z in range(chunk[1]*16, chunk[1]*16+16):
                # print(self.landmassinfo[(x, z)])
                biome = self.biomemap[(x, z)]
                for element in self.highmap[(x, z)]:
                    m = element[1]-element[0]
                    for i in range(m+1):
                        y = i + element[0]
                        if y >= element[2]:
                            decorators = biome.getTopDecorator(x, z, element[1] - element[0] + 1)
                            self.dimensionaccess.add_block((x, y, z), decorators[i], send_block_update=False,
                                                           check_visable_state=i == m, check_neightbors=False)
                        else:
                            self.dimensionaccess.add_block((x, y, z), biome.getDownerMaterial(),
                                                           send_block_update=False,
                                                           check_visable_state=False, check_neightbors=False)
        G.window.set_caption('Mcpython build ' + str(G.CONFIG["BUILD"]) + " | world generation | " + str(chunk) +
                             " | placing structures")
        features = []
        for x in range(chunk[0]*16, chunk[0]*16+16):
            for z in range(chunk[1]*16, chunk[1]*16+16):
                biome = self.biomemap[(x, z)]
                for feature in biome.FEATURE_LIST:
                    if feature not in features: features += [feature] * feature.get_paste_tries()
        x, z = chunk[0] * 16, chunk[1] * 16
        while len(features) > 0:
            ifeature = features.pop(0)
            nx = random.randint(0, 15) + x
            nz = random.randint(0, 15) + z
            coords = ifeature.get_possible_y_coordinates_for(nx, nz, self)
            if len(coords) > 0:
                ny = random.choice(coords)
                biome = self.biomemap[(nx, nz)]
                if random.randint(0, ifeature.get_properility()) == 0 and ifeature in biome.FEATURE_LIST:
                    ifeature.generate(nx, ny, nz, self)
        G.window.set_caption('Mcpython build ' + str(G.CONFIG["BUILD"]))

    def generate_chunks_in(self, start, end):
        for cx in range(start[0], end[0]+1):
            for cz in range(start[1], end[1]+1):
                self.generate_chunk((cx, cz))

