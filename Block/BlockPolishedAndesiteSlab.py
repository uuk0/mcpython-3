import globals as G
import Block.ISlab
import traceback


@G.blockhandler
class PolishedAndesiteSlab(Block.ISlab.ISlab):
    @staticmethod
    def getName():
        return "minecraft:polished_andesite_slab"
