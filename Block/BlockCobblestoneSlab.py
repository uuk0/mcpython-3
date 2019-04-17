import globals as G
import Block.ISlab
import traceback


@G.blockhandler
class CobbelstoneSlab(Block.ISlab.ISlab):
    @staticmethod
    def getName():
        return "minecraft:cobblestone_slab"
