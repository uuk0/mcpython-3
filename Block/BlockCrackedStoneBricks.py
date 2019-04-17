import globals as G
import Block.ISlab
import traceback


@G.blockhandler
class CrackedStoneBricks(Block.ISlab.ISlab):
    @staticmethod
    def getName():
        return "minecraft:cracked_stone_bricks"

