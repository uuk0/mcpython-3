
import Block.IBlock
import globals as G


@G.blockhandler
class Gravel(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:gravel"

    def get_drop(self):
        #todo: add flint
        return {self.getName(): 1}

