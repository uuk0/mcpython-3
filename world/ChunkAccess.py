import globals as G
import pyglet
import util.vector
import Block.IBlock


class ChunkAccess:
    @staticmethod
    def generate_chunk(chunk, dimensionaccess):
        dimensionaccess.worldgenerationprovider.generate_chunk(chunk)
        return ChunkAccess(chunk, dimensionaccess)

    def __init__(self, chunkaddress, dimensionprovider):
        self.dimensionaccess = dimensionprovider
        self.position = chunkaddress
        self.batch = pyglet.graphics.Batch()
        self.alpha_batch = pyglet.graphics.Batch()
        self.paticle_batch = pyglet.graphics.Batch()
        self.world = {}
        self.visable = False

    def draw(self):
        # todo: move to right events
        self.batch.draw()
        self.alpha_batch.draw()
        self.paticle_batch.draw()

    def add_block(self, position, block, check_visable_state=True, check_neightbors=True,
                  send_block_update=True, arguments=[[], {}]):
        if position in self.world:
            self.remove_block(position, check_neightbors=False, send_block_update=False)
        if type(block) == str:
            if block not in G.blockhandler.blocks:
                raise ValueError("can't access block named "+str(block))
            block = G.blockhandler.blocks[block](position,
                                                 *arguments[0], **arguments[1])
        elif type(block) not in G.blockhandler.blocks.values():
            try:
                if issubclass(type(block), Block.IBlock.IBlock):
                    block = block(util.vector.unrelative_position(position, self.position),
                                  *arguments[0], **arguments[1])
            except:
                raise ValueError("can't create any block from "+str(block))
        else:
            block.position = position
        self.world[position] = block
        block.on_create()
        block.position = position
        if check_visable_state:
            self.check_visable_state_of(position)
        if check_neightbors:
            self.check_surrounding_visable_state_of(position)
        if send_block_update:
            x, y, z = position
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    for dz in range(-1, 2):
                        if [dx, dy, dz].count(0) >= 2:
                            nx, ny, nz = x + dx, y + dy, z + dz
                            chunkaccess = G.worldaccess.get_active_dimension_access().get_chunk_for(
                                util.vector.sectorize((nx, ny, nz)))
                            iblock = chunkaccess.get_block((nx, ny, nz), raise_exc=False)
                            if iblock:
                                iblock.on_block_update(reason=position)

    def remove_block(self, position, check_neightbors=True, send_block_update=True):
        iblock = self.get_block(position, raise_exc=False)
        if not iblock: return
        self.hide_block(position)
        del self.world[position]
        iblock.on_delete()
        if check_neightbors:
            self.check_surrounding_visable_state_of(position)
        if send_block_update:
            x, y, z = position
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    for dz in range(-1, 2):
                        if [dx, dy, dz].count(0) >= 2:
                            nx, ny, nz = x + dx, y + dy, z + dz
                            chunkaccess = G.worldaccess.get_active_dimension_access().get_chunk_for(
                                util.vector.sectorize((nx, ny, nz)))
                            iblock = chunkaccess.get_block((nx, ny, nz), raise_exc=False)
                            if iblock:
                                iblock.on_block_update(reason=position)

    def check_visable_state_of(self, position):
        iblock = self.get_block(position, raise_exc=False)
        if iblock:
            iblock.on_visabel_state_check()
            state = self.is_block_visable(position)
            if state != iblock.is_visable:
                if state:
                    self.show_block(position)
                else:
                    self.hide_block(position)

    def check_surrounding_visable_state_of(self, position):
        x, y, z = position
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                for dz in range(-1, 2):
                    if [dx, dy, dz].count(0) >= 2:
                        nx, ny, nz = x + dx, y + dy, z + dz
                        chunkaccess = G.worldaccess.get_active_dimension_access().get_chunk_for(
                            util.vector.sectorize((nx, ny, nz)))
                        iblock = chunkaccess.get_block((nx, ny, nz), raise_exc=False)
                        if iblock:
                            iblock.on_visabel_state_check()
                            state = chunkaccess.is_block_visable((nx, ny, nz))
                            if state != iblock.is_visable:
                                if state:
                                    chunkaccess.show_block((nx, ny, nz))
                                else:
                                    chunkaccess.hide_block((nx, ny, nz))

    def show_block(self, position):
        iblock = self.get_block(position)
        if iblock:
            try:
                G.modelhandler.show(iblock)
            except:
                print(iblock)
                raise
        iblock.visable = True

    def hide_block(self, position):
        iblock = self.get_block(position)
        if iblock:
            G.modelhandler.hide(iblock)
        iblock.visable = False

    def is_block_visable(self, position) -> bool:
        x, y, z = position
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                for dz in range(-1, 2):
                    if [dx, dy, dz].count(0) == 2:
                        nx, ny, nz = x + dx, y + dy, z + dz
                        chunk = util.vector.sectorize((nx, ny, nz))
                        chunkaccess = self.dimensionaccess.get_chunk_for(chunk, generate=False, create=False)
                        if chunkaccess:
                            iblock = chunkaccess.get_block((nx, ny, nz), raise_exc=False)
                            if not (iblock and iblock.is_solid()):
                                return True
                        else:
                            return True
        return False

    def get_block(self, position, raise_exc=True):
        chunk = util.vector.sectorize(position)
        if chunk != self.position:
            return self.dimensionaccess.get_chunk_for(chunk, generate=False).get_block(position, raise_exc=raise_exc)
        if position not in self.world:
            if raise_exc:
                raise ValueError("position not in world")
            return None
        return self.world[position]



