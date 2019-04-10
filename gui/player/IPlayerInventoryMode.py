"""
base class for all inventorys that would like to be states of the player inventory
"""

import gui.Inventory
import pyglet.window.mouse
import globals as G


class IPlayerInventoryMode(gui.Inventory.Inventory):
    def on_close(self):
        G.player.playerinventory.set_mode("hotbar")

    def get_depend_inventory_parts(self):
        return []

    def is_only_esc_closed(self): return False

    def should_be_closed_by_esc(self): return True

    def on_event(self, name, *args, **kwargs):
        pass

    def set_position(self, position):
        for slot in self.slots:
            slot.move_relative(position)
        self.position = position
