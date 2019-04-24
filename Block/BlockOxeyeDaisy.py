import Block.IPlant
import globals as G


@G.blockhandler
class Cornflower(Block.IPlant.IPlant):
    @staticmethod
    def getName():
        return "minecraft:oxeye_daisy"

