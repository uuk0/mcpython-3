import Block.IBlock
import globals as G


@G.blockhandler
class EndStone(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:end_stone"

