import globals as G
import world.gen.feature.IFeature
import random
import math
import util.vector

NONE_BLOCKS = [None, "minecraft:air"]


class OreType(world.gen.feature.IFeature.IFeature):
    def __init__(self, oreblocks, minheight, maxheight, tries_per_chunk, min_size, max_size, replace=["minecraft:stone"]):
        self.oreblocks = oreblocks if type(oreblocks) in [list, tuple] else [oreblocks]
        self.minheight = minheight
        self.maxheight = maxheight
        self.tries_per_chunk = tries_per_chunk
        self.min_size = min_size
        self.max_size = max_size
        self.spawn_range = list(range(self.minheight, self.maxheight+1))
        self.replace = replace

    def generate(self, x, y, z, worldgenerationprovider):
        if self.min_size == self.max_size == 1:
            worldgenerationprovider.dimensionaccess.add_block((x, y, z), random.choice(self.oreblocks),
                                                              send_block_update=False,
                                                              check_visable_state=False, check_neightbors=False)
            return
        size = random.randint(self.min_size, self.max_size)
        sizea = size ** (1/3)
        if sizea <= 1:
            worldgenerationprovider.dimensionaccess.add_block((x, y, z), random.choice(self.oreblocks),
                                                              send_block_update=False,
                                                              check_visable_state=False, check_neightbors=False)
            return
        mx, mz = random.randint(1, round(sizea)), random.randint(1, round(sizea))
        my = round(size / ((4 / 3) * math.pi * mx * mz))
        if my == 0: my = 1
        for dx in range(-mx, mx+1):
            for dy in range(-my, my+1):
                for dz in range(-mz, mz+1):
                    if dx ** 2 / mx ** 2 + dy ** 2 / my ** 2 + dz ** 2 / mz ** 2 <= 1:
                        chunk = util.vector.sectorize((x + dx, 0, y + dy))
                        block = worldgenerationprovider.dimensionaccess.get_chunk_for(chunk, generate=False). \
                            get_block((x + dx, y + dy, z + dz), raise_exc=False)
                        if (not block and any([x in self.replace for x in NONE_BLOCKS])) or (block and block.getName()
                                                                                             in self.replace):
                            worldgenerationprovider.dimensionaccess.add_block((x+dx, y+dy, z+dz),
                                                                              random.choice(self.oreblocks),
                                                                              send_block_update=False,
                                                                              check_visable_state=False,
                                                                              check_neightbors=False)

    def get_possible_y_coordinates_for(self, x, z, worldgenerationprovider):
        return self.spawn_range

    def get_paste_tries(self):
        return self.tries_per_chunk if type(self.tries_per_chunk) not in [list, tuple] else \
            random.randint(*self.tries_per_chunk)

    def get_properility(self):
        return 1


COAL = OreType("minecraft:coal_ore", 0, 127, 20, 5, 17)
IRON = OreType("minecraft:iron_ore", 0, 63, 20, 4, 9)
GOLD = OreType("minecraft:gold_ore", 0, 31, 2, 1, 9)
EMERALD = OreType("minecraft:emerald_ore", 4, 31, [3, 8], 1, 1)
REDSTONE = OreType("minecraft:redstone_ore", 0, 15, 8, 2, 8)
DIAMOND = OreType("minecraft:diamond_ore", 0, 15, 1, 1, 9)
LAPIS = OreType("minecraft:lapis_ore", 0, 31, 1, 1, 7)

DEFAULT_ORES = [COAL, IRON, GOLD, REDSTONE, DIAMOND, LAPIS]

# other varianss

DIRT = OreType("minecraft:dirt", 0, 255, 10, 1, 33)
GRAVEL = OreType("minecraft:gravel", 0, 255, 8, 1, 33)
DIORITE = OreType("minecraft:diorite", 0, 80, 10, 1, 33)
GRANITE = OreType("minecraft:granite", 0, 80, 10, 1, 33)
ANDESITE = OreType("minecraft:andesite", 0, 80, 10, 1, 33)

DEFAULT_STONES = [DIRT, GRAVEL, DIORITE, GRANITE, ANDESITE]


class OreProvider:
    def __init__(self, ores=DEFAULT_ORES, extend=[]):
        self.ores = ores + extend

    def get_ores(self):
        return self.ores


DEFAULT_ORE_PROVIDER = OreProvider()
DEFAULT_STONE_PROVIDER = OreProvider(DEFAULT_STONES)

