import world.gen.structure.Structure
import random
import globals as G
import util.vector


class OreProvider(world.gen.structure.Structure.IHeightStructure):
    def __init__(self, ore_name, min_height, max_height, min_size, max_size, vein_amount, replace=["minecraft:stone"]):
        self.ore_name = ore_name
        self.min_height = min_height
        self.max_height = max_height
        self.min_size = min_size
        self.max_size = max_size
        self.vein_amount = vein_amount
        self.replace_blocks = replace
        self.oretable = {}

    def is_valid(self, x, y, z, height) -> bool:
        chunk = util.vector.sectorize((x, y, z))
        if chunk in self.oretable and self.oretable[chunk] > self.vein_amount:
            return False
        return True

    def paste(self, x, y, z):
        # print(x, y, z)
        chunk = util.vector.sectorize((x, y, z))
        if not chunk in self.oretable: self.oretable[chunk] = 1
        else: self.oretable[chunk] += 1
        sizex = round(random.randint(self.min_size, self.max_size) ** (1/3))
        sizey = round(random.randint(self.min_size, self.max_size) ** (1/3))
        sizez = round(random.randint(self.min_size, self.max_size) ** (1/3))
        amount = 0
        for dx in range(-sizex, sizex+1):
            for dy in range(-sizey, sizey+1):
                for dz in range(-sizez, sizez+1):
                    if (dx**2) / (sizex**2) + (dy**2) / (sizey**2) + (dz**2) / (sizez ** 2) <= 1:
                        rx, ry, rz = x + dx, y + dy, z + dz
                        if (rx, ry, rz) not in G.model.world and None in self.replace_blocks:
                            G.model.add_block((rx, ry, rz), self.ore_name)
                        elif (rx, ry, rz) in G.model.world and \
                                G.model.world[(rx, ry, rz)].getName() in self.replace_blocks:
                            G.model.add_block((rx, ry, rz), self.ore_name)

    def get_min(self) -> int:
        return self.min_height

    def get_max(self) -> int:
        return self.max_height

    def getStructureGenerationChance(self) -> int:
        return 1


COAL_ORE = OreProvider("minecraft:coal_ore", 0, 127, 4, 17, 20)
IRON_ORE = OreProvider("minecraft:iron_ore", 0, 63, 4, 9, 20)
GOLD_ORE = OreProvider("minecraft:gold_ore", 0, 31, 1, 9, 2)
EMERALD_ORE = OreProvider("minecraft:emerald_ore", 4, 31, 1, 1, 5)
REDSTONE_ORE = OreProvider("minecraft:redstone_ore", 0, 15, 2, 8, 2)
DIAMOND_ORE = OreProvider("minecraft:diamond_ore", 0, 15, 1, 9, 1)
LAPIS_ORE = OreProvider("minecraft:lapis_ore", 0, 31, 1, 7, 1)


