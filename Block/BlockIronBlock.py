import Block.IBlock
import globals as G


@G.blockhandler
class IronBlock(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:iron_block"

