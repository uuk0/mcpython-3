import globals as G
import Block.ISlab
import traceback


@G.blockhandler
class PolishedGraniteSlab(Block.ISlab.ISlab):
    @staticmethod
    def getName():
        return "minecraft:polished_granite_slab"
