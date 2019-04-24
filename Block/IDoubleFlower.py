import globals as G
import Block.IPlant
import util.vector


class IDoubleFlower(Block.IPlant.IPlant):
    def __init__(self, *args, placed_by_player=True, side="downer", **kwargs):
        Block.IPlant.IPlant.__init__(self, *args, **kwargs)
        self.side = "downer" if placed_by_player else side
        self.placed_by_player = placed_by_player

    def on_create(self):
        if self.placed_by_player:
            x, y, z = self.position
            G.worldaccess.get_active_dimension_access().add_block((x, y+1, z), self.getName(),
                                                                  arguments=[[], {"side": "upper",
                                                                                  "placed_by_player": False}])

    def get_active_model_index(self):
        return self.get_model_indexes()[0] if self.side == "upper" else self.get_model_indexes()[1]

    def get_model_indexes(self):  # upper, downer
        return [0, 1]

    def on_delete(self):
        x, y, z = self.position
        chunk = util.vector.sectorize(self.position)
        chunkaccess = G.worldaccess.get_active_dimension_access().get_chunk_for(chunk, generate=False)
        if self.side == "downer":
            if (x, y+1, z) in chunkaccess.world:
                chunkaccess.remove_block((x, y+1, z))
        else:
            if (x, y-1, z) in chunkaccess.world:
                chunkaccess.remove_block((x, y-1, z))

    @staticmethod
    def build_item():
        return False

    def can_player_walk_through(self):
        return True

    def get_ground_block(self):
        return ["minecraft:dirt", "minecraft:grass", self.getName()]

