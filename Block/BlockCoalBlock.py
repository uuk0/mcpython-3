
import Block.IBlock
import globals as G


@G.blockhandler
class CoalBlock(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:coal_block"

