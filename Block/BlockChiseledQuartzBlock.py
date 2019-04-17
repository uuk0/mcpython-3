import Block.IBlock
import globals as G


@G.blockhandler
class ChiseledQuartzBlock(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:chiseled_quartz_block"

