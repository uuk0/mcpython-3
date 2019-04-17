import Block.IBlock
import globals as G
import random


@G.blockhandler
class RedstoneOre(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:redstone_ore"

    def get_drop(self, itemstack):
        return {"minecraft:redstone": random.randint(4, 5)}

