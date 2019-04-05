
import Block.IBlock
import globals as G


@G.blockhandler
class OakLeaves(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:oak_leaves"

    def is_solid_to(self, position):
        return False

