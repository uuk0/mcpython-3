import time
import pyglet
import globals as G
import random
import util.vector


RANDOM_CHUNK_RANGE = 3


class TickHandler:
    def __init__(self):
        pyglet.clock.schedule_interval(self.game_tick, 0.05)
        self.active_tick = 0
        self.game_tick_shedule = {}

    def game_tick(self, dt):
        if self.active_tick in self.game_tick_shedule:
            functions = self.game_tick_shedule[self.active_tick]
            for function in functions:
                function[0](*function[1], **function[2])
        self.active_tick += 1
        cx, cz = util.vector.sectorize(G.window.position)
        for dx in range(-RANDOM_CHUNK_RANGE, RANDOM_CHUNK_RANGE+1):
            for dz in range(-RANDOM_CHUNK_RANGE, RANDOM_CHUNK_RANGE + 1):
                self.send_random_tick((cx+dx, cz+dz))

    def tick_function(self, function, ticks, *args, **kwargs):
        if ticks <= 0: return
        tick_todo = self.active_tick + ticks
        if tick_todo not in self.game_tick_shedule: self.game_tick_shedule[tick_todo] = []
        self.game_tick_shedule[tick_todo].append([function, args, kwargs])

    def send_random_tick(self, chunk, amount=3):
        x, z = chunk[0] * 16, chunk[1] * 16
        worldaccess = G.worldaccess.get_active_dimension_access()
        for _ in range(amount):
            dx, dy, dz = random.randint(0, 15), random.randint(0, 15), random.randint(0, 15)
            rx, ry, rz = x + dx, dy, z + dz
            iblock = worldaccess.get_block((rx, ry, rz), raise_exc=False)
            if iblock:
                # print("block", iblock, "getted at", (rx, ry, rz), "an random tick update")
                iblock.on_random_block_update()


handler = TickHandler()

