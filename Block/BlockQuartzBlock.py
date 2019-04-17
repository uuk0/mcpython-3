
import Block.IBlock
import globals as G


@G.blockhandler
class QuartzBLock(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:quartz_block"

