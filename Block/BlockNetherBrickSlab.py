import globals as G
import Block.ISlab
import traceback


@G.blockhandler
class NetherBrickSlab(Block.ISlab.ISlab):
    @staticmethod
    def getName():
        return "minecraft:nether_brick_slab"
