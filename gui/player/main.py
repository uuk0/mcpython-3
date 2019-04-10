import globals as G
import gui.player.IPlayerInventoryMode
import texture.TextureFactory
import pyglet
import gui.Slot
import crafting.CraftingHandler


class Main(gui.player.IPlayerInventoryMode.IPlayerInventoryMode):
    def __init__(self, main):
        self.main = main
        self.init((0, 0))
        self.bgimage = pyglet.image.load(G.local+"/tmp/gui/player/main.png")
        self.bgsprite = pyglet.sprite.Sprite(self.bgimage)

    def create_slots(self):
        x, y = self.position
        x -= texture.TextureFactory.main.size[0] / 2
        y -= texture.TextureFactory.main.size[1] / 2 - 70
        slots = []
        for i in range(9):
            slots.append(gui.Slot.SlotCopy(self.main.slots[i], position=(x + 11 + i * 36, y)))
        y += 44
        for i in range(9):
            slots.append(gui.Slot.Slot(position=(x + 11 + i * 36, y)))
        y += 36
        for i in range(9):
            slots.append(gui.Slot.Slot(position=(x + 11 + i * 36, y)))
        y += 36
        for i in range(9):
            slots.append(gui.Slot.Slot(position=(x + 11 + i * 36, y)))
        # armor slots
        slots.append(gui.Slot.Slot(position=(x + 11, y + 152), is_valid_item_function=self.valid_head))
        slots.append(gui.Slot.Slot(position=(x + 11, y + 152 - 36), is_valid_item_function=self.valid_body))
        slots.append(gui.Slot.Slot(position=(x + 11, y + 152 - 36 * 2), is_valid_item_function=self.valid_leggings))
        slots.append(gui.Slot.Slot(position=(x + 11, y + 152 - 36 * 3), is_valid_item_function=self.valid_shoes))
        # crafting slots
        slots.append(gui.Slot.Slot(position=(x + 11 + 5 * 36, y + 186 - 36 * 1.5), update_func=self.crafting_update))
        slots.append(gui.Slot.Slot(position=(x + 11 + 6 * 36, y + 186 - 36 * 1.5), update_func=self.crafting_update))
        slots.append(gui.Slot.Slot(position=(x + 11 + 5 * 36, y + 150 - 36 * 1.5), update_func=self.crafting_update))
        slots.append(gui.Slot.Slot(position=(x + 11 + 6 * 36, y + 150 - 36 * 1.5), update_func=self.crafting_update))
        # output
        slots.append(gui.Slot.Slot(position=(x + 13 + 8 * 36, y + 166 - 36 * 1.5), update_func=self.crafting_update,
                                   allow_player_interaction=False))
        return slots

    def crafting_update(self, slot):
        pass

    def valid_head(self, itemstack):
        return False

    def valid_body(self, itemstack):
        return False

    def valid_leggings(self, itemstack):
        return False

    def valid_shoes(self, itemstack):
        return False

    def draw_background(self):
        x, y = self.position
        x -= texture.TextureFactory.hotbar.size[0] / 2
        y -= texture.TextureFactory.hotbar.size[1] / 2 + 90
        self.bgsprite.position = (x, y)
        self.bgsprite.draw()

    def on_close(self):
        G.inventoryhandler.show_inventory(G.player.playerinventory.POSSIBLE_MODES["hotbar"])

