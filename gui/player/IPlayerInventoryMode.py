"""
base class for all inventorys that would like to be states of the player inventory
"""

import gui.Inventory
import pyglet.window.mouse


class IPlayerInventoryMode(gui.Inventory.Inventory):
    def get_depend_inventory_parts(self):
        return []

    def is_only_esc_closed(self): return False

    def on_event(self, name, *args, **kwargs):
        if name == "on_mouse_press":
            # handle mouse input
            if args[2] == pyglet.window.mouse.LEFT:
                pass
            elif args[2] == pyglet.window.mouse.RIGHT:
                pass
            elif args[2] == pyglet.window.mouse.MIDDLE:
                pass
        elif name == "on_mouse_motion" and False:  # only used when in special mode
            pass

    def set_position(self, position):
        for slot in self.slots:
            slot.move_relative(position)
        self.position = position

