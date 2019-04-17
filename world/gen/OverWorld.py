import world.gen.IWorldGenerator
import globals as G
import util.noise, util.vector
import random
import world.gen.CaveGenerator
import util.progressbar

BIOME_SIZE = 4
DEFAULT_LEVEL = 20


class OverWorld(world.gen.IWorldGenerator.IWorldGenerator):
    def __init__(self, *args, **kwargs):
        world.gen.IWorldGenerator.IWorldGenerator.__init__(self, *args, **kwargs)
        self.smooth_highmap = {}
        self.smooth_biomemap = {}

    def generate_biome_map(self, cx, cz):
        if (cx, cz) in self.chunk_steps: return
        self.chunk_steps[(cx, cz)] = 1
        for x in range(cx*16, cx*16+16):
            for z in range(cz*16, cz*16+16):
                value = (util.noise.noise(x/BIOME_SIZE/4, -12, z/BIOME_SIZE/4, BIOME_SIZE) * 5 +
                         util.noise.noise(x / BIOME_SIZE / 8 + 10, -12, z / BIOME_SIZE / 8 - 10, BIOME_SIZE**2)) / 6
                value = round(value*(len(G.biomehandler.biometable)+1))
                if value >= len(G.biomehandler.biometable): value = 0
                biome = G.biomehandler.biometable[value]
                self.biomemap[(x, z)] = biome

    def smooth_biome_map(self, cx, cz):
        if (cx, cz) in self.chunk_steps and self.chunk_steps[(cx, cz)] > 2: return
        self.chunk_steps[(cx, cz)] = 2
        for dx in range(-1, 2):
            for dz in range(-1, 2):
                if [dx, dz].count(0) == 1:
                    self.generate_biome_map(cx+dx, cz+dz)
        for x in range(cx*16, cx*16+16):
            for z in range(cz*16, cz*16+16):
                biome = self.biomemap[(x, z)]
                surrounding = self._get_surrounding_biomes(x, z)
                surrounding += [biome] * biome.getHighMapSmoothRate()
                sold = surrounding[:]
                surrounding.sort(key=lambda v: surrounding.count(v))
                surrounding = list(tuple(surrounding))
                if surrounding[0] == biome:
                    self.smooth_biomemap[(x, z)] = biome
                elif sold.count(surrounding[0]) / 2 <= sold.count(biome):
                    self.smooth_biomemap[(x, z)] = biome
                else:
                    self.smooth_biomemap[(x, z)] = surrounding[0]

    def _get_surrounding_biomes(self, x, z, r=1):
        array = []
        for dx in range(-r, r+1):
            for dz in range(-r, r+1):
                nx, nz = x + dx, z + dz
                if (nx, nz) in self.biomemap:
                    biome = self.biomemap[(nx, nz)]
                    array.append(biome)
        return array

    def generate_high_map(self, cx, cz):
        if (cx, cz) in self.chunk_steps and self.chunk_steps[(cx, cz)] > 3: return
        for x in range(cx*16, cx*16+16):
            for z in range(cz*16, cz*16+16):
                if not (x, z) in self.biomemap:
                    self.generate_biome_map(*util.vector.sectorize((x, 0, z)))
                    self.smooth_biome_map(*util.vector.sectorize((x, 0, z)))
                biome = self.smooth_biomemap[(x, z)] if (x, z) in self.smooth_biomemap else self.biomemap[(x, z)]
                ground = util.noise.noise(x/biome.getHighFactor(), -10, -z/biome.getHighFactor(), 10) * 2 - 1
                rhigh = ground * biome.getHighVariation()
                m = util.noise.noise(-x/biome.getBaseHighVariationFactor(), -20,
                                     z/biome.getBaseHighVariationFactor(), 20) * 2 - 1
                m *= biome.getBaseHighVariation()
                high = rhigh + biome.getBaseHigh() + m
                self.highmap[(x, z)] = round(high)

        self.chunk_steps[(cx, cz)] = 3

    def smooth_high_map(self, cx, cz):
        if (cx, cz) not in self.chunk_steps: return
        for dx in range(-1, 2):
            for dz in range(-1, 2):
                if [dx, dz].count(0) == 1:
                    if not (cx+dx, cz+dz) not in self.chunk_steps:
                        self.generate_biome_map(cx, cz)
                        self.smooth_biome_map(cx, cz)
                    if self.chunk_steps[(cx, cz)] < 4:
                        self.generate_high_map(cx+dx, cz+dz)
        for x in range(cx*16, cx*16+16):
            for z in range(cz*16, cz*16+16):
                surrouning = self._get_surrounding_highs(x, z)
                if not (x, z) in self.highmap:
                    self.generate_high_map(*util.vector.sectorize((x, 0, z)))
                if not (x, z) in self.smooth_biomemap:
                    self.generate_biome_map(*util.vector.sectorize((x, 0, z)))
                    self.smooth_biome_map(*util.vector.sectorize((x, 0, z)))
                high = self.highmap[(x, z)]
                if (x, z) in self.smooth_biomemap:
                    surrouning += [high] * self.smooth_biomemap[(x, z)].getHighMapSmoothRate()
                    self.smooth_highmap[(x, z)] = round(sum(surrouning) / len(surrouning))
                else:
                    self.smooth_highmap[(x, z)] = high
            self.chunk_steps[(cx, cz)] = 4

    def _get_surrounding_highs(self, x, z, r=7):
        array = []
        for dx in range(-r, r+1):
            for dz in range(-r, r+1):
                nx, nz = x + dx, z + dz
                if (nx, nz) in self.highmap:
                    high = self.highmap[(nx, nz)]
                    array.append(high)
        return array

    def generate_bedrock_layer(self, cx, cz):
        self.chunk_steps[(cx, cz)] = 5
        for x in range(cx*16, cx*16+16):
            for z in range(cz*16, cz*16+16):
                if not (x, z) in self.smooth_biomemap:
                    self.generate_biome_map(*util.vector.sectorize((x, 0, z)))
                    self.smooth_biome_map(*util.vector.sectorize((x, 0, z)))
                biome = self.smooth_biomemap[(x, z)] if (x, z) in self.smooth_biomemap else self.biomemap[(x, z)]
                if biome.getBedrockType() not in [None, "none", 0]:
                    G.model.add_block((x, 0, z), "bedrock")
                    if biome.getBedrockType() == "normal":
                        for y in range(0, 5):
                            if random.randint(1, 10) > 7:
                                G.model.add_block((x, y, z), "bedrock", immediate=False)

    def generate_stone_layer(self, cx, cz):
        self.chunk_steps[(cx, cz)] = 6
        for x in range(cx*16, cx*16+16):
            for z in range(cz*16, cz*16+16):
                biome = self.smooth_biomemap[(x, z)] if (x, z) in self.smooth_biomemap else self.biomemap[(x, z)]
                high = self.smooth_highmap[(x, z)]
                dh = high - round(util.noise.noise(x / 20, -12, z / 20, -10) *
                                  (biome.getTopLayerRange()[1] - biome.getTopLayerRange()[0]) +
                                  biome.getTopLayerRange()[0])
                for y in range(1, high+1):
                    if (x, y, z) not in G.model.world:
                        if y <= dh:
                            G.model.add_block((x, y, z), biome.getBaseMaterial(), immediate=False)
                        elif y != high:
                            G.model.add_block((x, y, z), biome.getDownerTopDecoration(x, y, z,
                                                                                      high-y, high - dh),
                                              immediate=False)
                        else:
                            G.model.add_block((x, y, z), biome.getTopDecorator())

    def generate_structure(self, cx, cz):
        self.chunk_steps[(cx, cz)] = 7
        for x in range(cx * 16, cx * 16 + 16):
            for z in range(cz * 16, cz * 16 + 16):
                ibiome = self.smooth_biomemap[(x, z)] if (x, z) in self.smooth_biomemap else self.biomemap[(x, z)]
                if ibiome.getStructureHeightAmount() < 1:
                    if random.randint(1, round(1/ibiome.getStructureHeightAmount())) == 1:
                        self.paste_structures(ibiome, x, z)
                else:
                    for _ in range(ibiome.getStructureHeightAmount()):
                        self.paste_structures(ibiome, x, z)

    def paste_structures(self, ibiome, x, z):
        structures = ibiome.getStructures()
        random.shuffle(structures)
        # print(structures)
        for istructure in structures:
            if random.randint(1, round(1/istructure.getStructureGenerationChance())) == 1:
                if istructure.getStructureType() == "surface":
                    y = self.smooth_highmap[(x, z)] + 1
                    if istructure.is_valid(x, y, z, y-1):
                        istructure.paste(x, y, z)
                        break
                elif istructure.getStructureType() == "height":
                    y = random.randint(istructure.get_min(), istructure.get_max())
                    if istructure.is_valid(x, y, z, self.smooth_highmap[(x, z)]):
                        istructure.paste(x, y, z)
                        break

    def generate_chunk(self, cx, cz):
        # missing: biome map, temperature map
        self.generate_biome_map(cx, cz)
        self.smooth_biome_map(cx, cz)
        self.generate_high_map(cx, cz)
        self.smooth_high_map(cx, cz)
        self.generate_bedrock_layer(cx, cz)
        self.generate_stone_layer(cx, cz)
        world.gen.CaveGenerator.generate_chunk(cx, cz)
        self.generate_structure(cx, cz)

    def generate_area(self, start, end):
        print(" -generating biome map")
        for cx in range(start[0], end[0]+1):
            for cz in range(start[1], end[1]+1):
                self.generate_biome_map(cx, cz)
        print(" -smoothing biome map")
        for cx in range(start[0], end[0]+1):
            for cz in range(start[1], end[1]+1):
                self.smooth_biome_map(cx, cz)
        print(" -generating high map")
        for cx in range(start[0], end[0]+1):
            for cz in range(start[1], end[1]+1):
                self.generate_high_map(cx, cz)
        print(" -smoothing high map")
        for cx in range(start[0], end[0]+1):
            for cz in range(start[1], end[1]+1):
                self.smooth_high_map(cx, cz)
        print(" -placing blocks")
        size = abs(start[0] - end[0]) * abs(start[1] - end[1])
        util.progressbar.print_progress_bar(0, size, prefix='Progress:', suffix='Complete', length=size)
        for cx in range(start[0], end[0]+1):
            for cz in range(start[1], end[1]+1):
                util.progressbar.print_progress_bar(cx * 16 + cz, size, prefix='Progress:', suffix='Complete',
                                                    length=size)
                # print(cx, cz)
                self.generate_bedrock_layer(cx, cz)
                self.generate_stone_layer(cx, cz)
        print("\n -generating caves")
        for cx in range(start[0], end[0] + 1):
            for cz in range(start[1], end[1] + 1):
                print(cx, cz)
                world.gen.CaveGenerator.generate_chunk(cx, cz)
        print(" -placing structures")
        for cx in range(start[0], end[0] + 1):
            for cz in range(start[1], end[1] + 1):
                print(cx, cz)
                self.generate_structure(cx, cz)

