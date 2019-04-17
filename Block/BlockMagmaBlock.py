import Block.IBlock
import globals as G


@G.blockhandler
class MagmaBlock(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:magma_block"

