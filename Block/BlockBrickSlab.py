import globals as G
import Block.ISlab
import traceback


@G.blockhandler
class BrickSlab(Block.ISlab.ISlab):
    @staticmethod
    def getName():
        return "minecraft:brick_slab"
