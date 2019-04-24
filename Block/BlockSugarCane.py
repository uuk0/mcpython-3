import Block.IPlant
import globals as G


@G.blockhandler
class Cornflower(Block.IPlant.IPlant):
    @staticmethod
    def getName():
        return "minecraft:sugar_cane"

    def get_ground_block(self):
        return ["minecraft:dirt", "minecraft:grass", "minecraft:sand", self.getName()]

