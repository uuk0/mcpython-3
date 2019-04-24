import Block.IPlant
import globals as G


@G.blockhandler
class WitherRose(Block.IPlant.IPlant):
    @staticmethod
    def getName():
        return "minecraft:wither_rose"

