import gui.Inventory
import gui.player.IPlayerInventoryMode
import pyglet.image
import globals as G
import texture.TextureFactory
import gui.Slot


class Hotbar(gui.player.IPlayerInventoryMode.IPlayerInventoryMode):
    def __init__(self):
        self.init((0, 0))
        self.bgimage = pyglet.image.load(G.local+"/tmp/gui/player/hotbar.png")
        self.bgsprite = pyglet.sprite.Sprite(self.bgimage)
        self.slimage = pyglet.image.load(G.local+"/tmp/gui/player/hotbar_select.png")
        self.slsprite = pyglet.sprite.Sprite(self.slimage)

    def create_slots(self):
        x, y = self.position
        x -= texture.TextureFactory.Info.hotbar_size[0] / 2
        y -= texture.TextureFactory.Info.hotbar_size[1] / 2 + 200
        slots = []
        for i in range(9):
            slots.append(gui.Slot.Slot(position=(x+7+i*40, y+5)))
        return slots

    def draw_background(self):
        x, y = self.position
        x -= texture.TextureFactory.Info.hotbar_size[0] / 2
        y -= texture.TextureFactory.Info.hotbar_size[1] / 2 + 200
        self.bgsprite.position = (x, y)
        self.bgsprite.draw()

    def draw_overlay(self):
        x, y = self.position
        x -= texture.TextureFactory.Info.hotbar_size[0] / 2 + 2 - G.player.selectedinventoryslot * 40
        y -= texture.TextureFactory.Info.hotbar_size[1] / 2 + 202
        self.slsprite.position = (x, y)
        self.slsprite.draw()
        for slot in self.slots:
            if slot.get_stack().itemfile:
                slot.label.draw()

    def is_blocking_interaction(self):
        return False

    def get_setable_slots(self):
        return []

