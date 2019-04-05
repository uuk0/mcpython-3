import globals as G
import pyglet
import PIL.Image
import gui.Inventory
import gui.InventoryHandler
import Item.ItemHandler
import os
import Block.BlockHandler

os.makedirs(G.local+"/tmp/items")


class BlockItemFactory:
    def __init__(self):
        self.blocktable = G.blockhandler.blockarray[:]
        self.closed = False
        self.blockname = None

    def step(self):
        if self.closed: return
        if self.blockname:
            pyglet.image.get_buffer_manager().get_color_buffer().save(
                G.local+"/tmp/items/"+"_".join(self.blockname.split(":"))+".png")
            image = PIL.Image.open(G.local+"/tmp/items/"+"_".join(self.blockname.split(":"))+".png")
            image = image.crop((150, 60, 660, 515))
            image.save(G.local+"/tmp/items/"+"_".join(self.blockname.split(":"))+".png")
            G.itemhandler.register([self.blockname, G.local+"/tmp/items/"+"_".join(self.blockname.split(":"))+".png"])
        if len(self.blocktable) == 0:
            self.close()
            return
        block = self.blocktable.pop(0)
        name = block.getName()
        G.model.add_block((0, 0, 0), name)
        mname = G.model.world[(0, 0, 0)].get_model_name()
        if mname in G.modelhandler.modelindex:
            model = G.modelhandler.modelindex[mname]
            modelentry = model.entrys[G.model.world[(0, 0, 0)].get_active_model_index()]
            box = modelentry.data["box_size"] if "box_size" in modelentry.data else (0.5, 0.5, 0.5)
            G.window.positon = (1, 1.25+(box[1]*2-1), 1)
        else:
            G.window.position = (1, 1.25, 1)
        self.blockname = name

    def close(self):
        self.closed = True
        G.model.remove_block((0, 0, 0))

    def close_M(self):
        G.inventoryhandler.hide_inventory(dummyinventoryblockitemfactory)
        G.model.initialize()
        G.inventoryhandler.show_inventory(G.model.player.playerinventory)
        G.model.player.playerinventory.set_mode("hotbar")
        G.window.position = (0, 50, 0)
        G.window.rotation = (0, 0)
        pyglet.gl.glClearColor(0.5, 0.69, 1.0, 1)
        G.window.set_exclusive_mouse(True)


blockitemfactory = BlockItemFactory()


class DummyInventoryBlockItemFactory(gui.Inventory.Inventory):
    timer = 0

    def __init__(self):
        self.init((0, 0))
        self.label1 = pyglet.text.Label(text="generating world", color=(0, 0, 0, 255))

    def on_open(self):
        G.window.position = (1, 0.75, 1)
        G.window.rotation = (-45, -45)
        size = G.window.get_size()
        self.label1.position = (size[0] / 2, size[1] / 2)
        G.window.set_exclusive_mouse(False)

    def on_event(self, name, *args, **kwargs):
        if name == "update":
            self.timer += args[0]
            if self.timer > 1:
                self.timer -= 1
                blockitemfactory.step()
        elif name == "draw_3d_start":
            pyglet.gl.glClearColor(1.0, 1.0, 1.0, 0.0)
        elif name == "draw_2d_end":
            if blockitemfactory.closed:
                self.label1.draw()
                blockitemfactory.close_M()


dummyinventoryblockitemfactory = DummyInventoryBlockItemFactory()

