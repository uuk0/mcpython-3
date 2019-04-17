import Block.IBlock
import globals as G
import random


@G.blockhandler
class LapisOre(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:lapis_ore"

    def get_drop(self, itemstack):
        return {"minecraft:lapis_lazuli": random.randint(4, 8)}

