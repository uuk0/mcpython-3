import globals as G
import Block.ISlab
import traceback


@G.blockhandler
class DioriteSlab(Block.ISlab.ISlab):
    @staticmethod
    def getName():
        return "minecraft:diorite_slab"

