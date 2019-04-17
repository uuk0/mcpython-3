import opensimplex
import random
import globals as G
import util.progressbar
import util.vector

noise = opensimplex.OpenSimplex(G.CONFIG["seed"] * 100 - 10)


ENTRYS_PER_CHUNK = (5, 2)

ENTRACE_MAP = {}
PERLIN_MAP = {}
PERLIN_SIZE_RANGE = (3, 9)
PERLIN_DIRECTTION_RANGE = (-2, 2)


def cut_circle(x, y, z, size):
    # print(x, y, z)
    x, y, z = round(x), round(y), round(z)
    s = round(size)
    for dx in range(-s, s+1):
        for dy in range(-s, s+1):
            for dz in range(-s, s+1):
                pos = (x+dx, y+dy, z+dz)
                if dx**2 + dy**2 + dz**2 <= size and (pos not in G.model.world or
                                                      G.model.world[pos].getName() != "minecraft:bedrock"):
                    G.model.remove_block(pos)


def generate_chunk(cx, cz):
    entraces = round(noise.noise4d(cx, -1000, cz, 702)) * ENTRYS_PER_CHUNK[0] + ENTRYS_PER_CHUNK[1]
    ENTRACE_MAP[(cx, cz)] = []
    for i in range(entraces):
        x = round(noise.noise4d(cx, i*1000, cz, -100) * 8 + 8) + cx * 16
        z = round(noise.noise4d(cx, i*1000, cz, -1000*i) * 8 + 8) + cz * 16
        high = G.model.worldgenerator.smooth_highmap[(x, z)]
        y = round(noise.noise4d(cx, i*1000, cz, 12498237*i**2) * high / 2 + high / 2)
        worm = PerlinWorm((x, y, z), i)
        ENTRACE_MAP[(cx, cz)].append(worm)
    for worm in ENTRACE_MAP[(cx, cz)][:]:
        newchunk = (cx, cz)
        i = 0
        while (worm in ENTRACE_MAP[(cx, cz)] or (newchunk in G.model.worldgenerator.chunk_steps
                                                 and G.model.worldgenerator.chunk_steps[newchunk] >= 7)) and i < 100:
            # print(worm.position)
            worm.step()
            newchunk = util.vector.sectorize(worm.position)
            i += 1


class PerlinWorm:
    def __init__(self, position, cnumber):
        self.position = None
        self.update_position(None, position)
        self.seed = position[0] * position[1] * position[2] * (cnumber + 1)
        self.direction = (0, 0, 0)
        self.size = 3

    def update_position(self, oldpos, newpos):
        if newpos != None:
            chunkold = util.vector.sectorize(oldpos) if oldpos else None
            chunknew = util.vector.sectorize(newpos)
            if chunkold != chunknew:
                if chunkold in PERLIN_MAP and self in PERLIN_MAP[chunkold]:
                    PERLIN_MAP[chunkold].remove(self)
                if chunknew not in PERLIN_MAP: PERLIN_MAP[chunknew] = []
                if self not in PERLIN_MAP[chunknew]: PERLIN_MAP[chunknew].append(self)
        self.position = newpos

    def step(self):
        oldpos = self.position
        x, y, z = self.position
        cut_circle(x, y, z, self.size)
        v = noise.noise4d(x, y, z, self.seed*self.size*x*y*z) * 2
        self.size = self.in_range_helper(self.size, v, PERLIN_SIZE_RANGE)
        """if v > 0:
            if self.size + v > PERLIN_SIZE_RANGE[1]:
                self.size -= v
            else:
                self.size += v
        else:
            if self.size + v < PERLIN_SIZE_RANGE[0]:
                self.size -= v
            else:
                self.size += v"""
        dx = random.randint(-1, 1)  # noise.noise4d(x / 5, y / 5, z / 5, 702702) * 4
        dy = random.randint(-1, 1)  # noise.noise4d(x / 5, y / 5, z / 5, 702702) * 4
        dz = random.randint(-1, 1)  # noise.noise4d(x / 5, y / 5, z / 5, 702702) * 4
        rx, ry, rz = self.direction
        rx = self.in_range_helper(rx, dx, PERLIN_DIRECTTION_RANGE)
        ry = self.in_range_helper(ry, dy, PERLIN_DIRECTTION_RANGE)
        rz = self.in_range_helper(rz, dz, PERLIN_DIRECTTION_RANGE)
        x += rx
        if ry > 0:
            if y + ry > 255:
                y -= ry
            else:
                y += ry
        else:
            if y - ry < 0:
                y -= ry
            else:
                y += ry
        z += rz
        self.direction = (rx, ry, rz)
        # print((x, y, z), (rx, ry, rz), (dx, dy, dz), self.size)
        self.update_position(oldpos, (x, y, z))

    def in_range_helper(self, value, addition, ra):
        if addition > 0:
            if value + addition > ra[1]:
                return value - addition
            else:
                return value + addition
        else:
            if value + addition < ra[0]:
                return value - addition
            else:
                return value + addition
