
import Block.IBlock
import globals as G
import random


@G.blockhandler
class OakLeaves(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:oak_leaves"

    def is_solid_to(self, position):
        return False

    def get_drop(self):
        # todo: add sapling
        return {"minecraft:apple": 1} if random.randint(1, 20) == 1 else {}

