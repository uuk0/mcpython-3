import Block.IPlant
import globals as G
import random


@G.blockhandler
class Dandelion(Block.IPlant.IPlant):
    @staticmethod
    def getName():
        return "minecraft:dead_bush"

    def get_ground_block(self):
        return ["minecraft:sand"]
    
    def get_drop(self, itemstack):
        amount = random.randint(0, 2)
        if amount > 0: return {"minecraft:stick": amount}
        return {}

