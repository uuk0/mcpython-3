import globals as G
import Block.ISlab
import traceback


@G.blockhandler
class GraniteSlab(Block.ISlab.ISlab):
    @staticmethod
    def getName():
        return "minecraft:granite_slab"
