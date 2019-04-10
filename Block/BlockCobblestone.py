import Block.IBlock
import globals as G


@G.blockhandler
class CobbleStone(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:cobblestone"

