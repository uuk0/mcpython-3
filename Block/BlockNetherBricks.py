import Block.IBlock
import globals as G


@G.blockhandler
class NetherBricks(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:nether_bricks"

