import Block.IBlock
import globals as G
import util.vector


@G.blockhandler
class SnowLayer(Block.IBlock.IBlock):
    def __init__(self, *args, layer=1, **kwargs):
        Block.IBlock.IBlock.__init__(self, *args, **kwargs)
        self.layer = layer

    def on_block_update(self, reason=None):
        x, y, z = self.position
        if (x, y - 1, z) not in G.worldaccess.get_active_dimension_access().get_chunk_for(
                util.vector.sectorize(self.position)).world or \
                not G.worldaccess.get_active_dimension_access().get_chunk_for(
                    util.vector.sectorize(self.position)).world[(x, y-1, z)].is_solid():
            G.player.add_block_drop_to_inventory(self)
            G.worldaccess.remove_block(0, self.position)

    @staticmethod
    def getName():
        return "minecraft:snow_layer"

    def get_active_model_index(self):
        return 0  # self.layer - 1

    def can_interact_with(self, itemstack, mousekey=None, mousemod=None):
        return itemstack.item and itemstack.itemname == "minecraft:snow" and self.layer != 8

    def on_interact_with(self, itemstack, mousekey=None, mousemod=None):
        itemstack.amount -= 1
        self.layer += 1
        return itemstack, False

    def get_drop(self, itemstack):
        """
        :return: an itemname: amount dict that should be given to player
        """
        return {"minecraft:snow": self.layer} if self.layer != 8 else {"minecraft:snow_block": 1}

    def is_solid(self):
        return False

