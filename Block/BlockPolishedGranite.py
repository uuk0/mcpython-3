import Block.IBlock
import globals as G


@G.blockhandler
class PolishedGranite(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:polished_granite"

