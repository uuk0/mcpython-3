import Block.IDoubleFlower
import globals as G


@G.blockhandler
class Lilac(Block.IDoubleFlower.IDoubleFlower):
    @staticmethod
    def getName():
        return "minecraft:lilac"

    def is_solid(self):
        return False

