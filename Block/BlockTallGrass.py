import Block.IDoubleFlower
import globals as G
import random


@G.blockhandler
class TallGrass(Block.IDoubleFlower.IDoubleFlower):
    @staticmethod
    def getName():
        return "minecraft:tall_grass"

    def get_drop(self, itemstack):
        return {"minecraft:seed": 1} if random.randint(1, 3) == 1 else {}

