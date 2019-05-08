import world.gen.feature.structure.ITopLayerStructure
import random
import globals as G


class SpruceTree(world.gen.feature.structure.ITopLayerStructure.ITopLayerStructure):
    def __init__(self, tries, properility):
        world.gen.feature.structure.ITopLayerStructure.ITopLayerStructure.__init__(self)
        self.paste_tries = tries
        self.properility = properility

    def generate(self, x, y, z, worldgenerationprovider):
        high = random.randint(5, 10)
        for dy in range(high):
            worldgenerationprovider.dimensionaccess.add_block((x, y+dy, z), "minecraft:spruce_log")
            if dy // 2 == 0 and dy > 4:
                width = 2
                for dx in range(-width, width+1):
                    for dz in range(-width, width+1):
                        if not dx == dz == 0:
                            worldgenerationprovider.dimensionaccess.add_block((x + dx, y + dy, z + dz),
                                                                              "minecraft:spruce_leaves")

    def get_paste_tries(self):
        return self.paste_tries

    def get_properility(self):
        return self.properility

