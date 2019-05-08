import util.vertices
import globals as G
import util.vector


class IBlock:
    """
    basic class for all blocks
    """

    def __init__(self, position, previous=None, hitposition=None):
        self.position = position
        self.previous = previous
        self.hitposition = hitposition
        self.is_visable = None
        self.shown_data = None
        self.injected_redstone_value = 0
        # self.on_create()

    def inject_redstone_value(self, value):
        if value > 15 or value < 0: return  # value range!!!
        if not self.is_redstone_power_able(): return
        if value > self.injected_redstone_value:
            self.injected_redstone_value = value
        chunkaccess = G.worldaccess.get_active_dimension_access().get_chunk_for_position(self.position)
        x, y, z = self.position
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                for dz in range(-1, 2):
                    if [dx, dy, dz].count(0) >= 2:
                        nx, ny, nz = x + dx, y + dy, z + dz
                        chunkaccess = G.worldaccess.get_active_dimension_access().get_chunk_for(
                            util.vector.sectorize((nx, ny, nz)))
                        iblock = chunkaccess.get_block((nx, ny, nz), raise_exc=False)
                        if iblock:
                            iblock.on_block_update(reason=self.position)
        self.on_redstone_update()

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

    def is_redstone_power_able(self): return self.is_solid()

    def on_redstone_update(self):
        pass

    def on_random_block_update(self):
        pass

