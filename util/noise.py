import opensimplex
import globals as G

noise_object = opensimplex.OpenSimplex(seed=G.CONFIG["seed"])


def noise(x, y, z, seed, dimension=0):
    return noise_object.noise4d(x, y, z, seed*(dimension+seed)+dimension+seed) / 2 + 0.5

