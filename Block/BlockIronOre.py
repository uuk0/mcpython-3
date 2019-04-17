import Block.IBlock
import globals as G


@G.blockhandler
class IronOre(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:iron_ore"

