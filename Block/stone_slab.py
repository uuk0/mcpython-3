import globals as G
import Block.IBlock
import traceback


@G.blockhandler
class UpperStoneSlab(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:stone_slab_upper"

    def is_solid_to(self, position):
        return False


@G.blockhandler
class DownerStoneSlab(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:stone_slab_downer"

    def is_solid_to(self, position):
        traceback.print_stack()
        return False

