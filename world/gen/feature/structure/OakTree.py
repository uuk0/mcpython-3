import world.gen.feature.structure.ITree
import random


def place_big_oak_tree(self, x, y, z, worldgenerationprovider):
    random.seed(x * y * z)
    log_type = "minecraft:oak_log"
    random.seed(y / x / z if x != 0 and z != 0 else y)
    height = random.randint(6, 10)
    for dy in range(height-3):
        worldgenerationprovider.dimensionaccess.add_block((x, y + dy, z), log_type)
    for dy in range(height-3, height):
        for _ in range(random.randint(1, 3)):
            dx, dz = random.randint(-3, 3), random.randint(-3, 3)
            worldgenerationprovider.dimensionaccess.add_block((x+dx, y + dy, z+dz), log_type)
    self.generate_hill(self.getLeaveBlock(), x, y + round(height / 3 * 2), z, height - round(height / 3 * 2) + 2, 4,
                       worldgenerationprovider)


class OakTree(world.gen.feature.structure.ITree.ITree):
    def __init__(self, *args, propertility=3, big_oak_tee_chance=0, **kwargs):
        world.gen.feature.structure.ITree.ITree.__init__(self, *args, **kwargs)
        self.spawn_propertility = propertility
        self.big_oak_tree_chance = big_oak_tee_chance

    def generate(self, x, y, z, worldgenerationprovider):
        if self.big_oak_tree_chance != 0 and random.randint(1, self.big_oak_tree_chance) == 1:
            place_big_oak_tree(self, x, y, z, worldgenerationprovider)
        else:
            world.gen.feature.structure.ITree.ITree.generate(self, x, y, z, worldgenerationprovider)

    def get_log_types(self):
        return ["minecraft:oak_log"]  # a list of all possible log types. will be random selected

    def getLeaveBlock(self):
        return "minecraft:oak_leaves"

    def get_paste_tries(self):
        return 10

    def get_properility(self):
        return self.spawn_propertility


DEFAULT = OakTree(minheight=4, maxheight=6, propertility=30)
PLAINS = OakTree(minheight=4, maxheight=6, propertility=10, big_oak_tee_chance=3)

