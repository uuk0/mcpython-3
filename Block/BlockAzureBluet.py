import Block.IPlant
import globals as G


@G.blockhandler
class Dandelion(Block.IPlant.IPlant):
    @staticmethod
    def getName():
        return "minecraft:azure_bluet"

