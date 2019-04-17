
import Block.IBlock
import globals as G
import random


@G.blockhandler
class Brick(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:bookshelf"

    def get_drop(self, itemstack):
        return {"minecraft:book": random.randint(1, 2)}

