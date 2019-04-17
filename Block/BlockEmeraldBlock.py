import Block.IBlock
import globals as G


@G.blockhandler
class EmeraldBlock(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:emerald_block"

