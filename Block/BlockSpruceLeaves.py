
import Block.IBlock
import globals as G
import random


@G.blockhandler
class SpruceLeaves(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:spruce_leaves"

    def is_solid(self):
        return False

    def get_drop(self, itemstack):
        # todo: add sapling
        return {}

