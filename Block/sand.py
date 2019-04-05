import Block.IBlock
import globals as G


@G.blockhandler
class Sand(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:sand"

