import util.vertices
import globals as G


class IBlock:
    """
    basic class for all blocks
    """

    def __init__(self, position):
        self.position = position
        self.on_create()

    def on_create(self):
        pass

    def on_delete(self):
        pass

    def is_solid_to(self, position):
        return True

    def isBrakeAble(self):
        """
        todo: add player & item given overwrite
        :return: if the block can be broken by the player
        """
        return True

    @staticmethod
    def getName():
        """
        :return: the name as the block should be accessable
        """
        return "minecraft:NONE"

    def get_active_model_index(self):
        return 0

    def get_model_name(self):
        return self.getName()

    def can_interact_with(self, itemstack, mousekey=None, mousemod=None):
        """
        callen when an item is used onto the block
        """
        return False

    def on_interact_with(self, itemstack, mousekey=None, mousemod=None):
        """
        callen to interact with the given item
        :return: (either the itemstack or the itemstack to replace with, do some more work)
        """
        return itemstack, True

    def get_drop(self):
        """
        :return: an itemname: amount dict that should be given to player
        """
        return {self.getName(): 1}
