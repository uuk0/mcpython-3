import Block.IBlock
import globals as G


@G.blockhandler
class Grass(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:grass"

    def get_drop(self, itemstack):
        return {"minecraft:dirt": 1}

