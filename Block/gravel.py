
import Block.IBlock
import globals as G


@G.blockhandler
class Gravel(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:gravel"

