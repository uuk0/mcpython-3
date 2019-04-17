import Block.IBlock
import globals as G


@G.blockhandler
class Netherrack(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:netherrack"

