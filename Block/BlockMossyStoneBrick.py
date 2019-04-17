import Block.IBlock
import globals as G


@G.blockhandler
class MossyStoneBricks(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:mossy_stone_bricks"

