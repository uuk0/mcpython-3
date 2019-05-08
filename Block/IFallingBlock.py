import globals as G
import Block.IBlock
import TickHandler


class IFallingBlock(Block.IBlock.IBlock):
    def on_block_update(self, reason=None):
        chunkaccess = G.worldaccess.get_active_dimension_access().get_chunk_for_position(self.position)
        x, y, z = self.position
        iblock = chunkaccess.get_block((x, y-1, z), raise_exc=False)
        if not iblock:
            TickHandler.handler.tick_function(self.fall, 4)

    def fall(self):
        chunkaccess = G.worldaccess.get_active_dimension_access().get_chunk_for_position(self.position)
        x, y, z = self.position
        iblock = chunkaccess.get_block((x, y - 1, z), raise_exc=False)
        if not iblock:
            chunkaccess.remove_block(self.position)
            chunkaccess.add_block((x, y-1, z), self)


