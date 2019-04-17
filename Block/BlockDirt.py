
import Block.IBlock
import globals as G


@G.blockhandler
class Dirt(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:dirt"

