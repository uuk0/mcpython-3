import Block.IBlock
import globals as G


@G.blockhandler
class EmeraldOre(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:emerald_ore"

    def get_drop(self, itemstack):
        return {"minecraft:emerald": 1}

