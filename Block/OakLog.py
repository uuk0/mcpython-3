
import Block.IBlock
import globals as G


@G.blockhandler
class OakLog(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:oak_log"

