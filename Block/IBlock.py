import util.vertices
import globals as G


class IBlock:
    """
    basic class for all blocks
    """

    def __init__(self, position, previous=None, hitposition=None):
        self.position = position
        self.previous = previous
        self.hitposition = hitposition
        self.is_visable = None  # todo: implement these to system
        self.shown_data = None
        # self.on_create()

    def on_visabel_state_check(self):
        pass

    def on_block_update(self, reason=None):
        """
        :param reason: an position why the blockupdate is callen. may be None
        """
        pass

    def on_create(self):
        pass

    def on_delete(self):
        pass

    def is_solid(self):
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

    def get_drop(self, itemstack):
        """
        :return: an itemname: amount dict that should be given to player
        """
        return {self.getName(): 1}

    @staticmethod
    def build_item(): return True

    def can_player_walk_through(self): return False
