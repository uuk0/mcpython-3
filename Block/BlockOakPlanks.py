
import Block.IBlock
import globals as G


@G.blockhandler
class OakLeaves(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:oak_planks"

