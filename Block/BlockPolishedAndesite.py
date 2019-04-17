import Block.IBlock
import globals as G


@G.blockhandler
class PolishedAndesite(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:polished_andesite"

