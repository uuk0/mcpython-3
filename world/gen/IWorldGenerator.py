"""
Main file for all stuff around WorldGeneration base class
"""

import globals as G


class IWorldGenerator:
    def __init__(self):
        self.highmap = {}
        self.biomemap = {}
        self.chunk_steps = {}

    def generate_chunk(self, cx, cz):
        raise NotImplementedError()

