import Block.IBlock
import globals as G


@G.blockhandler
class Stone(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:stone"

    def get_drop(self):
        return {"minecraft:cobblestone": 1}

