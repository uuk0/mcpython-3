import globals as G
import Block.ISlab
import traceback


@G.blockhandler
class EndStoneBrickSlab(Block.ISlab.ISlab):
    @staticmethod
    def getName():
        return "minecraft:end_stone_brick_slab"
