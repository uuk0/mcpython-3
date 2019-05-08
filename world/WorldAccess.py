import globals as G
import random
import world.DimensionAccess
import world.player
import util.vector


SEED_LIMIT = 2 ** 64 / 2


class WorldAccess:
    def __init__(self, name=None, seed=None):
        G.worldaccess = self
        self.name = name
        if not seed: seed = random.randint(-SEED_LIMIT, SEED_LIMIT)
        print("world seed: "+str(seed))
        self.seed = seed
        self.dimensions = {}
        self.player = world.player.Player()

    def create_dimension_from_id(self, ID):
        self.dimensions[ID] = world.DimensionAccess.DimensionAccess(self, ID)

    def add_block(self, dimension, position, block, check_visable_state=True, check_neightbors=True,
                  send_block_update=True, arguments=[[], {}]):
        if dimension not in self.dimensions: raise ValueError("unknown dimension "+str(dimension))
        self.dimensions[dimension].add_block(position, block, check_visable_state, check_neightbors, send_block_update,
                                             arguments)

    def remove_block(self, dimension, position, check_neightbors=True, send_block_update=True):
        if dimension not in self.dimensions: raise ValueError("unknown dimension "+str(dimension))
        chunk = util.vector.sectorize(position)
        self.dimensions[dimension].get_chunk_for(chunk, generate=False).remove_block(position, check_neightbors,
                                                                                     send_block_update)

    def draw_normal(self):
        dimensionaccess = self.get_active_dimension_access()
        for chunkaccess in dimensionaccess.chunks.values():
            if chunkaccess.visable:
                chunkaccess.batch.draw()

    def draw_alpha(self):
        dimensionaccess = self.get_active_dimension_access()
        for chunkaccess in dimensionaccess.chunks.values():
            if chunkaccess.visable:
                chunkaccess.alpha_batch.draw()

    def draw_particle(self):
        dimensionaccess = self.get_active_dimension_access()
        for chunkaccess in dimensionaccess.chunks.values():
            if chunkaccess.visable:
                chunkaccess.paticle_batch.draw()

    def hit_test(self, position, vector, max_distance=8, exact_hit=False):
        """ Line of sight search from current position. If a block is
        intersected it is returned, along with the block previously in the line
        of sight. If no block is found, return None, None.

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position to check visibility from.
        vector : tuple of len 3
            The line of sight vector.
        max_distance : int
            How many blocks away to search for a hit.

        """
        m = 30
        x, y, z = position
        y += 0.5
        dx, dy, dz = vector
        previous = None
        for _ in range(max_distance * m):
            key = util.vector.normalize((x, y, z))
            chunk = util.vector.sectorize(key)
            chunkaccess = self.get_active_dimension_access().get_chunk_for(chunk, generate=False,
                                                                           create=False)
            if chunkaccess and key in chunkaccess.world:
                iblock = chunkaccess.world[key]
                modelentry = G.modelhandler.modelindex[iblock.get_model_name()].entrys[iblock.get_active_model_index()]
                if modelentry.is_part_of((x, y, z)):
                    return (key, previous) if not exact_hit else (key, previous, (x, y, z))
            if previous != key:
                previous = key
            x, y, z = x + dx / m, y + dy / m, z + dz / m
        return (None, None) if not exact_hit else (None, None, None)

    def get_active_dimension_access(self) -> world.DimensionAccess.DimensionAccess:
        return self.dimensions[self.player.dimension]

    def cleanup(self):
        for dim in self.dimensions.values():
            dim.cleanup()

    def change_sectors(self, before, after):
        """ Move from sector `before` to sector `after`. A sector is a
        contiguous x, y sub-region of world. Sectors are used to speed up
        world rendering.

        """
        before_set = set()
        after_set = set()
        pad = 4
        for dx in range(-pad, pad + 1):
            for dz in range(-pad, pad + 1):
                if dx ** 2 + dz ** 2 > (pad + 1) ** 2:
                    continue
                if before:
                    x, z = before
                    before_set.add((x + dx, z + dz))
                if after:
                    x, z = after
                    after_set.add((x + dx, z + dz))
        show = after_set - before_set
        hide = before_set - after_set
        for sector in show:
            chunkaccess = self.get_active_dimension_access().get_chunk_for(sector, generate=False)  # here: autogenerate
            chunkaccess.visable = True
        for sector in hide:
            chunkaccess = self.get_active_dimension_access().get_chunk_for(sector)
            chunkaccess.visable = False

    def get_block(self, position, **kwargs):
        return self.get_active_dimension_access().get_chunk_for(util.vector.sectorize(position)).get_block(position, **kwargs)

