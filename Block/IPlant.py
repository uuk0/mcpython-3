import Block.IBlock
import globals as G
import util.vector


class IPlant(Block.IBlock.IBlock):
    def __init__(self, *args, **kwargs):
        Block.IBlock.IBlock.__init__(self, *args, **kwargs)

    def on_block_update(self, reason=None):
        x, y, z = self.position
        chunk = util.vector.sectorize(self.position)
        iblock = G.worldaccess.get_active_dimension_access().get_chunk_for(chunk).get_block((x, y - 1, z),
                                                                                            raise_exc=False)
        if not iblock or iblock.getName() not in self.get_ground_block():
            G.worldaccess.remove_block(G.player.dimension, self.position)
            # todo: change to drop
            G.player.add_block_drop_to_inventory(self)

    @staticmethod
    def build_item():
        return False

    def can_player_walk_through(self):
        return True

    def is_solid(self):
        return False

    def get_ground_block(self):
        return ["minecraft:dirt", "minecraft:grass"]

