import globals as G
import Block.ISlab
import traceback


@G.blockhandler
class PolishedDioriteSlab(Block.ISlab.ISlab):
    @staticmethod
    def getName():
        return "minecraft:polished_diorite_slab"
