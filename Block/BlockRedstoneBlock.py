import Block.IBlock
import globals as G


@G.blockhandler
class RedstoneBlock(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:redstone_block"

