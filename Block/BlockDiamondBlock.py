
import Block.IBlock
import globals as G


@G.blockhandler
class DiamondBlock(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:diamond_block"

