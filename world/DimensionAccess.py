import globals as G
import util.vector
import world.ChunkAccess
import world.gen.WorldGenerationProvider


class DimensionAccess:
    def __init__(self, worldprovider, ID=0):
        self.ID = ID
        self.chunks = {}
        self.worldprovider = worldprovider
        self.worldgenerationprovider = world.gen.WorldGenerationProvider.WorldGenerationProvider(self,
                                                                                        seed=self.worldprovider.seed)

    def add_block(self, position, block, check_visable_state=True, check_neightbors=True,
                  send_block_update=True, arguments=[[], {}]):
        chunk = util.vector.sectorize(position)
        if chunk not in self.chunks: self.chunks[chunk] = world.ChunkAccess.ChunkAccess.generate_chunk(chunk, self)
        self.chunks[chunk].add_block(position, block,
                                     check_visable_state, check_neightbors, send_block_update, arguments)

    def get_chunk_for(self, chunk, generate=True, create=True) -> world.ChunkAccess.ChunkAccess:
        if chunk not in self.chunks:
            if not create:
                return None
            if generate:
                self.chunks[chunk] = world.ChunkAccess.ChunkAccess.generate_chunk(chunk, self)
            else:
                self.chunks[chunk] = world.ChunkAccess.ChunkAccess(chunk, self)
        return self.chunks[chunk]

    def cleanup(self):
        self.chunks = {}

    def get_chunk_for_position(self, position, generate=True, create=True) -> world.ChunkAccess.ChunkAccess:
        return self.get_chunk_for(util.vector.sectorize(position), generate=generate, create=create)

    def get_block(self, position, raise_exc=True):
        return self.get_chunk_for_position(position, generate=False).get_block(position, raise_exc=raise_exc)

