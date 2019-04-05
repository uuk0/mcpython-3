import globals as G
import world.gen.structure.Structure
import util.noise


class ITreeStructure(world.gen.structure.Structure.IStructure):
    def __init__(self):
        pass

    def paste(self, x, y, z):
        r = self.getHighRange()
        high = round(util.noise.noise(x, -y, z, -10) * (r[1] - r[1]) + r[0])
        for ry in range(high):
            G.model.add_block((x, y+ry, z), self.getLogBlock())
        self.generateLeaves(high, x, y, z)

    def generateLeaves(self, high, x, y, z):
        self.generate_hill(self.getLeaveBlock(), x, y+round(high/3*2), z, high-round(high/3*2)+2, 2)

    @staticmethod
    def getLogBlock():
        return None

    @staticmethod
    def getHighRange():
        raise NotImplementedError()

    @staticmethod
    def getLeaveBlock():
        return None

    @staticmethod
    def generate_hill(material, x, y, z, h, s, taper=1):
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
                    if not (x, y, z) in G.model.world:
                        G.model.add_block((x, y, z), t)
            s -= d  # decrement side lenth so hills taper off

