import Block.IPlant
import globals as G
import random


@G.blockhandler
class GrassSmall(Block.IPlant.IPlant):
    @staticmethod
    def getName():
        return "minecraft:grass_small"

    def get_drop(self, itemstack):
        return {"minecraft:seed": 1} if random.randint(1, 3) == 1 else {}
