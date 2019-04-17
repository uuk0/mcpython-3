import globals as G
import Block.ISlab
import traceback


@G.blockhandler
class MossyStoneBrickSlab(Block.ISlab.ISlab):
    @staticmethod
    def getName():
        return "minecraft:mossy_stone_brick_slab"
