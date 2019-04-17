import globals as G
import Block.ISlab
import traceback


@G.blockhandler
class StoneSlab(Block.ISlab.ISlab):
    @staticmethod
    def getName():
        return "minecraft:stone_slab"
