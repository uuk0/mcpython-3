import Block.IDoubleFlower
import globals as G


@G.blockhandler
class Lilac(Block.IDoubleFlower.IDoubleFlower):
    @staticmethod
    def getName():
        return "minecraft:rose_bush"

    def is_solid(self):
        return False

