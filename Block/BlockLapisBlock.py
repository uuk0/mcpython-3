import Block.IBlock
import globals as G


@G.blockhandler
class LapisBlock(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:lapis_block"

