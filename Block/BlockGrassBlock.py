import Block.IBlock
import globals as G
import util.vector


@G.blockhandler
class Grass(Block.IBlock.IBlock):
    @staticmethod
    def getName():
        return "minecraft:grass"

    def get_drop(self, itemstack):
        return {"minecraft:dirt": 1}

    def on_block_update(self, reason=None):
        pass

    def get_active_model_index(self):
        x, y, z = self.position
        chunkaccess = G.worldaccess.get_active_dimension_access().get_chunk_for(util.vector.sectorize(self.position),
                                                                                generate=False)
        if (x, y+1, z) in chunkaccess.world and chunkaccess.world[(x, y+1, z)].getName() == "minecraft:snow_layer":
            return 1
        return 0

