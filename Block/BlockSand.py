import Block.IFallingBlock
import globals as G


@G.blockhandler
class Sand(Block.IFallingBlock.IFallingBlock):
    @staticmethod
    def getName():
        return "minecraft:sand"

