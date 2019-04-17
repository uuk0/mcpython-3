import Block.IBlock
import globals as G


@G.blockhandler
class NetherQuartzOre(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:nether_quartz_ore"

    def get_drop(self, itemstack):
        return {"minecraft:quartz": 1}

