
import Block.IFallingBlock
import globals as G


@G.blockhandler
class Gravel(Block.IFallingBlock.IFallingBlock):
    @staticmethod
    def getName():
        return "minecraft:gravel"

    def get_drop(self, itemstack):
        # todo: add flint
        return {self.getName(): 1}

