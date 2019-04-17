
import Block.IBlock
import globals as G


@G.blockhandler
class GoldBlock(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:gold_block"

