import Block.IBlock
import globals as G


@G.blockhandler
class Granite(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:granite"

