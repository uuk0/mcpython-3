
import Block.IBlock
import globals as G


@G.blockhandler
class GoldOre(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:gold_ore"

