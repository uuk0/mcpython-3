import Block.IPlant
import globals as G
import world.gen.feature.structure.OakTree
import TickHandler


@G.blockhandler
class OakSapling(Block.IPlant.IPlant):
    def __init__(self, *args, **kwargs):
        Block.IPlant.IPlant.__init__(self, *args, **kwargs)
        self.stage = 0

    @staticmethod
    def getName():
        return "minecraft:oak_sapling"

    def on_random_block_update(self):
        self.stage += 1
        print(self.stage)
        if self.stage == 7:
            x, y, z = self.position
            world.gen.feature.structure.OakTree.DEFAULT.generate(x, y, z, G.worldaccess.get_active_dimension_access().
                                                                 worldgenerationprovider)

