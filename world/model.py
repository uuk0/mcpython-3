import pyglet
import config
import globals as G
from collections import deque
import random
import util.vector
import util.vertices
import time
import world.gen.IWorldGenerator
import world.gen.OverWorld
import world.player


class Model(object):

    def __init__(self):

        G.model = self

        # A Batch is a collection of vertex lists for batched rendering.
        self.batch = pyglet.graphics.Batch()
        self.alpha_batch = pyglet.graphics.Batch()

        # A mapping from position to the texture of the block at that position.
        # This defines all the blocks that are currently in the world.
        self.world = {}

        # Same mapping as `world` but only contains blocks that are shown.
        self.shown = {}

        # Mapping from position to a pyglet `VertextList` for all shown blocks.
        self._shown = {}

        # Mapping from sector to a list of positions inside that sector.
        self.sectors = {}

        self.player = world.player.Player()

        # Simple function queue implementation. The queue is populated with
        # _show_block() and _hide_block() calls
        self.queue = deque()

        self.worldgenerator = world.gen.OverWorld.OverWorld()

        # self._initialize()

    def initialize(self):
        """ Initialize the world by placing all the blocks.

        """
        print("generating world")
        self.worldgenerator.generate_area((-1, -1), (1, 1))
        print("world generation finished")
        """
        n = 80  # 1/2 width and height of world
        s = 1  # step size
        y = 0  # initial y height
        for x in range(-n, n + 1, s):
            for z in range(-n, n + 1, s):
                # create a layer stone an grass everywhere.
                self.add_block((x, y - 2, z), "grass", immediate=False)
                self.add_block((x, y - 3, z), "bedrock", immediate=False)
                if x in (-n, n) or z in (-n, n):
                    # create outer walls.
                    for dy in range(-2, 3):
                        self.add_block((x, y + dy, z), "bedrock", immediate=False)

        # generate the hills randomly
        o = n - 10
        for _ in range(120):
            a = random.randint(-o, o)  # x position of the hill
            b = random.randint(-o, o)  # z position of the hill
            c = -1  # base of the hill
            h = random.randint(1, 6)  # height of the hill
            s = random.randint(4, 8)  # 2 * s is the side length of the hill
            d = 1  # how quickly to taper off the hills
            t = random.choice(["grass", "sand", "brick", "stone"])
            for y in range(c, c + h):
                for x in range(a - s, a + s + 1):
                    for z in range(b - s, b + s + 1):
                        if (x - a) ** 2 + (z - b) ** 2 > (s + 1) ** 2:
                            continue
                        if (x - 0) ** 2 + (z - 0) ** 2 < 5 ** 2:
                            continue
                        self.add_block((x, y, z), t, immediate=False)
                s -= d  # decrement side lenth so hills taper off"""

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
            if key in self.world:
                iblock = self.world[key]
                modelentry = G.modelhandler.modelindex[iblock.get_model_name()].entrys[iblock.get_active_model_index()]
                if modelentry.is_part_of((x, y, z)):
                    return (key, previous) if not exact_hit else (key, previous, (x, y, z))
                """box = modelentry.data["box_size"] if "box_size" in modelentry.data else (0.5, 0.5, 0.5)
                rpos = modelentry.data["relative_position"] if "relative_position" in modelentry.data else (0, 0, 0)
                mx, my, mz = key
                sx, sy, sz = mx + box[0] + rpos[0], my + box[1] + rpos[1], mz + box[2] + rpos[2]
                ex, ey, ez = mx - box[0] + rpos[0], my - box[1] + rpos[1], mz - box[2] + rpos[2]
                if sx > ex: ex, sx = sx, ex
                if sy > ey: ey, sy = sy, ey
                if sz > ez: ez, sz = sz, ez
                # print((sx, x, ex), (sy, y, ey), (sz, z, ez))
                if sx <= x <= ex and sy <= y <= ey and sz <= z <= ez:
                    return key, previous"""
            if previous != key:
                previous = key
            x, y, z = x + dx / m, y + dy / m, z + dz / m
        return (None, None) if not exact_hit else (None, None, None)

    def exposed(self, position):
        """ Returns False is given `position` is surrounded on all 6 sides by
        blocks, True otherwise.

        """
        x, y, z = position
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                for dz in range(-1, 2):
                    if [dx, dy, dz].count(0) == 2:
                        npos = (x+dx, y+dy, z+dz)
                        if npos not in G.model.world: return True
                        if not G.model.world[npos].is_solid_to(position): return True
        return False

    def add_block(self, position, blockname, immediate=True, previous=None, hitposition=None, args=[], kwargs={}):
        """ Add a block with the given `texture` and `position` to the world.

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position of the block to add.
        blockname : the name of the block to add
        immediate : bool
            Whether or not to draw the block immediately.

        """
        if position[1] < 0 or position[1] > 255: return
        if position in self.world:
            self.remove_block(position, immediate)
        block = G.blockhandler.create_block_at(position, blockname, *args,
                                               previous=previous, hitposition=hitposition, *kwargs)
        if block:
            self.world[position] = block
            self.sectors.setdefault(util.vector.sectorize(position), []).append(position)
            if immediate:
                if self.exposed(position):
                    self.show_block(position)
                self.check_neighbors(position)

    def remove_block(self, position, immediate=True):
        """ Remove the block at the given `position`.

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position of the block to remove.
        immediate : bool
            Whether or not to immediately remove block from canvas.

        """
        if position not in self.world: return
        self.world[position].on_delete()
        self.sectors[util.vector.sectorize(position)].remove(position)
        if immediate:
            if position in self.shown:
                self.hide_block(position)
            self.check_neighbors(position, removed=True)
        del self.world[position]

    def check_neighbors(self, position, removed=False):
        """ Check all blocks surrounding `position` and ensure their visual
        state is current. This means hiding blocks that are not exposed and
        ensuring that all exposed blocks are shown. Usually used after a block
        is added or removed.

        """
        x, y, z = position
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                for dz in range(-1, 2):
                    if [dx, dy, dz].count(0) == 2:
                        npos = (x+dx, y+dy, z+dz)
                        if npos in G.model.world:
                            if self.exposed(npos) or position not in G.model.world or removed:
                                self.show_block(npos)
                            else:
                                self.hide_block(npos)

    def show_block(self, position, immediate=True):
        """ Show the block at the given `position`. This method assumes the
        block has already been added with add_block()

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position of the block to show.
        immediate : bool
            Whether or not to show the block immediately.

        """
        block = self.world[position]
        self.shown[position] = block
        if immediate:
            self._show_block(position, block)
        else:
            self._enqueue(self._show_block, position, block)

    def _show_block(self, position, block):
        """ Private implementation of the `show_block()` method.

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position of the block to show.
        texture : list of len 3
            The coordinates of the texture squares. Use `tex_coords()` to
            generate.

        """
        G.modelhandler.show(position)
        """
        x, y, z = position
        vertex_data = util.vertices.cube_vertices(x, y, z, 0.5)
        texture_data = list(util.vertices.tex_coords(*block.getTextureData()))
        # create vertex list
        # FIXME Maybe `add_indexed()` should be used instead
        self._shown[position] = self.batch.add(24, pyglet.gl.GL_QUADS, self.group,
                                               ('v3f/static', vertex_data),
                                               ('t2f/static', texture_data))"""

    def hide_block(self, position, immediate=True):
        """ Hide the block at the given `position`. Hiding does not remove the
        block from the world.

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position of the block to hide.
        immediate : bool
            Whether or not to immediately remove the block from the canvas.

        """
        if position in self.shown:
            self.shown.pop(position)
        if immediate:
            self._hide_block(position)
        else:
            self._enqueue(self._hide_block, position)

    def _hide_block(self, position):
        """ Private implementation of the 'hide_block()` method.

        """
        G.modelhandler.hide(position)
        """
        self._shown.pop(position).delete()
        """

    def update_block(self, position):
        state = position in self.shown
        if state:
            self.hide_block(position)
            self.show_block(position)

    def show_sector(self, sector):
        """ Ensure all blocks in the given sector that should be shown are
        drawn to the canvas.

        """
        for position in self.sectors.get(sector, []):
            if position not in self.shown and self.exposed(position):
                self.show_block(position, False)

    def hide_sector(self, sector):
        """ Ensure all blocks in the given sector that should be hidden are
        removed from the canvas.

        """
        for position in self.sectors.get(sector, []):
            if position in self.shown:
                self.hide_block(position, False)

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
            self.show_sector(sector)
        for sector in hide:
            self.hide_sector(sector)

    def _enqueue(self, func, *args):
        """ Add `func` to the internal queue.

        """
        self.queue.append((func, args))

    def _dequeue(self):
        """ Pop the top function from the internal queue and call it.

        """
        func, args = self.queue.popleft()
        func(*args)

    def process_queue(self):
        """ Process the entire queue while taking periodic breaks. This allows
        the game loop to run smoothly. The queue contains calls to
        _show_block() and _hide_block() so this method should be called if
        add_block() or remove_block() was called with immediate=False

        """
        start = time.clock()
        while self.queue and time.clock() - start < 1.0 / G.CONFIG["TICKS_PER_SEC"]:
            self._dequeue()

    def process_entire_queue(self):
        """ Process the entire queue with no breaks.

        """
        while self.queue:
            self._dequeue()

