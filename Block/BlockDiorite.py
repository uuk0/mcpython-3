
import Block.IBlock
import globals as G


@G.blockhandler
class Diorite(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:diorite"

