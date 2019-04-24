import world.gen.feature.structure.ITopLayerStructure
import random
import util.vector


class ITree(world.gen.feature.structure.ITopLayerStructure.ITopLayerStructure):
    def __init__(self, minheight=3, maxheight=7):
        self.height_range = [minheight, maxheight]

    def generate(self, x, y, z, worldgenerationprovider):
        random.seed(x*y*z)
        log_type = random.choice(self.get_log_types())
        random.seed(y/x/z if x != 0 and z != 0 else y)
        height = random.randint(*self.height_range)
        for dy in range(height):
            worldgenerationprovider.dimensionaccess.add_block((x, y+dy, z), log_type)
        self.generateLeaves(height, x, y, z, worldgenerationprovider)

    def generateLeaves(self, high, x, y, z, worldgenerationprovider):
        self.generate_hill(self.getLeaveBlock(), x, y + round(high / 3 * 2), z, high - round(high / 3 * 2) + 2, 2,
                           worldgenerationprovider)

    @staticmethod
    def generate_hill(material, x, y, z, h, s, worldgenerationprovider, taper=1):
        # code from orginal world gen
        a = x
        b = z
        c = y
        d = taper  # how quickly to taper off the hills
        t = material
        for y in range(c, c + h):
            for x in range(a - s, a + s + 1):
                for z in range(b - s, b + s + 1):
                    if (x - a) ** 2 + (z - b) ** 2 > (s + 1) ** 2:
                        continue
                    if (x - 0) ** 2 + (z - 0) ** 2 < 5 ** 2:
                        continue
                    chunk = util.vector.sectorize((x, y, z))
                    if not (x, y, z) in worldgenerationprovider.dimensionaccess.get_chunk_for(chunk, generate=False).\
                            world:
                        worldgenerationprovider.dimensionaccess.add_block((x, y, z), t)
            s -= d  # decrement side lenth so hills taper off

    def get_log_types(self):
        return []  # a list of all possible log types. will be random selected

    def getLeaveBlock(self):
        return None
