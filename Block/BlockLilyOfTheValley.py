import Block.IPlant
import globals as G


@G.blockhandler
class Cornflower(Block.IPlant.IPlant):
    @staticmethod
    def getName():
        return "minecraft:lily_of_the_valley"

