import globals as G
import Block.ISlab
import traceback


@G.blockhandler
class AndesiteSlab(Block.ISlab.ISlab):
    @staticmethod
    def getName():
        return "minecraft:andesite_slab"

