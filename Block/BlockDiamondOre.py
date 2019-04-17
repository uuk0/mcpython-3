
import Block.IBlock
import globals as G


@G.blockhandler
class DiamondOre(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:diamond_ore"

    def get_drop(self, itemstack):
        return {"minecraft:diamond": 1}

