"""
an biome border generator
"""

import opensimplex
import random
import PIL.Image


ZOOM = 60
BORDER_SIZE = 40


class BiomeBorderGenerator:
    def __init__(self, noiseseeds=(random.randint(0, 10000000), random.randint(0, 10000000),)):
        self.basenoise = opensimplex.OpenSimplex(noiseseeds[0])
        self.basenoise2 = opensimplex.OpenSimplex(noiseseeds[1])
        self.bordermap = {}

    def generate_for_chunk(self, chunk):
        x, z = chunk
        self.generate_map_for(x * 16 - 2, z * 16 - 2, x * 16 + 18, z * 16 + 18)

    def generate_map_for(self, startx, startz, endx, endz):
        for x in range(startx, endx+1):
            for z in range(startz, endz+1):
                self.bordermap[(x, z)] = self.get_smooth_value(x, z)

    def get_base_noise_value_at(self, x, z):
        x /= ZOOM
        z /= ZOOM
        value1 = self.basenoise.noise2d(x, z)
        return round(abs(value1) * BORDER_SIZE) == 0

    def get_smooth_value(self, x, z):
        value = self.get_base_noise_value_at(x, z)
        s = []
        for dx in range(-1, 2):
            for dz in range(-1, 2):
                if [dx, dz].count(0) < 2:
                    s.append(self.get_base_noise_value_at(x+dx, z+dz))
        if s.count(False) < 5:
            return False
        return value

    def generate_border_image_an_save_at(self, save):
        keymap = list(self.bordermap.keys())
        xmap = [e[0] for e in keymap]
        zmap = [e[1] for e in keymap]
        maxx, minx = max(xmap), min(xmap)
        maxz, minz = max(zmap), min(zmap)
        size = (maxx - minx + 1, maxz - minz + 1)
        image = PIL.Image.new("RGB", size)
        for x in range(minx, maxx+1):
            for z in range(minz, maxz+1):
                rx, rz = abs(minx + x), abs(minz + z)
                if (x, z) in self.bordermap:
                    image.putpixel((rx, rz), (0, 255, 0) if self.bordermap[(x, z)] else (255, 0, 0))
        image.save(save)

