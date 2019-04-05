import gui.Inventory
import gui.player.IPlayerInventoryMode
import pyglet.image
import globals as G


class Hotbar(gui.player.IPlayerInventoryMode.IPlayerInventoryMode):
    def __init__(self):
        self.init((0, 0))
        self.bgimage = pyglet.image.load(G.local+"/tmp/gui/player/hotbar.png")

    def draw_background(self):
        self.bgimage.blit(*self.position)

