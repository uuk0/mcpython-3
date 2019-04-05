
import Block.IBlock
import globals as G


@G.blockhandler
class Brick(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:dirt"

