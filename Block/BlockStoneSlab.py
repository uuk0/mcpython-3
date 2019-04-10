import globals as G
import Block.IBlock
import traceback


@G.blockhandler
class UpperStoneSlab(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:stone_slab_upper"

    def is_solid_to(self, position):
        return False

    def can_interact_with(self, itemstack, mousekey=None, mousemod=None):
        return itemstack.itemname == "minecraft:stone_slab_downer"

    def on_interact_with(self, itemstack, mousekey=None, mousemod=None):
        itemstack.amount -= 1
        G.model.add_block(self.position, "minecraft:double_stone_slab")
        return itemstack, False


@G.blockhandler
class DownerStoneSlab(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:stone_slab_downer"

    def is_solid_to(self, position):
        return False

    def can_interact_with(self, itemstack, mousekey=None, mousemod=None):
        return itemstack.itemname == "minecraft:stone_slab_upper"

    def on_interact_with(self, itemstack, mousekey=None, mousemod=None):
        itemstack.amount -= 1
        G.model.add_block(self.position, "minecraft:double_stone_slab")
        return itemstack, False


@G.blockhandler
class DoubleStoneSlab(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:double_stone_slab"

    def get_model_name(self):
        return "minecraft:stone"

    def get_drop(self):
        return {"minecraft:stone_slab_upper": 1, "minecraft:stone_slab_downer": 1}

