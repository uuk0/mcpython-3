import Block.IBlock
import globals as G


@G.blockhandler
class EndStoneBricks(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:end_stone_bricks"

