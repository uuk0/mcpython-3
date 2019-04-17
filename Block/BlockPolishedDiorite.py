import Block.IBlock
import globals as G


@G.blockhandler
class PolishedDiorite(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:polished_diorite"

