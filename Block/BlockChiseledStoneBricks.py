import globals as G
import Block.IBlock


@G.blockhandler
class ChiseledStoneBricks(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:chiseled_stone_bricks"

