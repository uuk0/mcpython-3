
import Block.IBlock
import globals as G


@G.blockhandler
class CoalOre(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:coal_ore"

    def get_drop(self, itemstack):
        return {"minecraft:coal": 1}

