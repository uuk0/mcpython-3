import globals as G
import pyglet
import PIL.Image
import gui.Inventory
import gui.InventoryHandler
import Item.ItemHandler
import os
import Block.BlockHandler
import sys
import world.WorldAccess

os.makedirs(G.local+"/tmp/items")

ENABLE_ITEM_GEN = True
ITEM_GEN_TIME = 0.5


class BlockItemFactory:
    def __init__(self):
        self.blocktable = []
        self.maxlenght = None
        self.closed = False
        self.blockname = None
        self.chunkaccess = None

    def step(self):
        if self.closed: return
        if self.blockname:
            if ENABLE_ITEM_GEN:
                pyglet.image.get_buffer_manager().get_color_buffer().save(
                    G.local+"/tmp/items/"+"_".join(self.blockname.split(":"))+".png")
                image = PIL.Image.open(G.local+"/tmp/items/"+"_".join(self.blockname.split(":"))+".png")
                image = image.crop((150, 60, 660, 515))
                image = image.resize((32, 32))
                image.save(G.local+"/tmp/items/"+"_".join(self.blockname.split(":"))+".png")
                G.itemhandler.register([self.blockname,
                                        G.local+"/tmp/items/"+"_".join(self.blockname.split(":"))+".png"])
            else:
                missing = PIL.Image.open(G.local + "/tmp/missing_texture.png")
                # missing.resize((32, 32))
                missing.save(G.local + "/tmp/items/missing_texture.png")
                G.itemhandler.register([self.blockname,
                                        G.local + "/tmp/items/missing_texture.png"])
        if len(self.blocktable) == 0:
            self.close()
            return
        G.window.set_caption('Mcpython build ' + str(G.CONFIG["BUILD"]) + " | building blocks | " +
                             str(self.maxlenght - len(self.blocktable) + 1) + " / " + str(self.maxlenght))
        self.chunkaccess = G.worldaccess.get_active_dimension_access().get_chunk_for((0, 0), generate=False)
        block = self.blocktable.pop(0)
        name = block.getName()
        if ENABLE_ITEM_GEN:
            self.chunkaccess.add_block((0, 0, 0), name, send_block_update=False)
        else:
            dummyinventoryblockitemfactory.timer = 1
        mname = self.chunkaccess.world[(0, 0, 0)].get_model_name() if ENABLE_ITEM_GEN else None
        if mname in G.modelhandler.modelindex and ENABLE_ITEM_GEN:
            model = G.modelhandler.modelindex[mname]
            # (model.name, self.chunkaccess.world[(0, 0, 0)].getName(), model.entrys, model.data)
            modelentry = model.entrys[self.chunkaccess.world[(0, 0, 0)].get_active_model_index()]
            box = modelentry.data["box_size"] if "box_size" in modelentry.data else (0.5, 0.5, 0.5)
            G.window.positon = (1, 1.25+(box[1]*2-1), 1)
        else:
            G.window.position = (1, 1.25, 1)
        self.blockname = name

    def close(self):
        self.chunkaccess = G.worldaccess.get_active_dimension_access().get_chunk_for((0, 0), generate=False)
        self.closed = True
        self.chunkaccess.remove_block((0, 0, 0))

    def close_M(self):
        G.window.set_caption('Mcpython build '+str(G.CONFIG["BUILD"])+" | world generation")
        G.inventoryhandler.hide_inventory(dummyinventoryblockitemfactory)
        pyglet.gl.glClearColor(0.5, 0.69, 1.0, 1)
        G.worldaccess.get_active_dimension_access().worldgenerationprovider.generate_chunks_in((-1, -1), (1, 1))
        G.worldaccess.change_sectors(G.window.sector, None)
        G.worldaccess.change_sectors(None, G.window.sector)
        G.inventoryhandler.show_inventory(G.player.playerinventory)
        G.player.playerinventory.set_mode("hotbar")
        G.window.position = (0, G.worldaccess.get_active_dimension_access().worldgenerationprovider.highmap[(0, 0)
                                    ][-1][1]+2, 0)
        G.window.rotation = (0, 0)
        pyglet.gl.glClearColor(0.5, 0.69, 1.0, 1)
        G.window.set_exclusive_mouse(True)
        G.window.set_caption('Mcpython build '+str(G.CONFIG["BUILD"]))


blockitemfactory = BlockItemFactory()


class DummyInventoryBlockItemFactory(gui.Inventory.IInventoryBlocking):
    timer = 0

    def __init__(self):
        self.init((0, 0))
        self.label1 = pyglet.text.Label(text="generating world", color=(0, 0, 0, 255))

    def on_open(self):
        print("opening blockitemfactory")
        G.window.position = (1, 0.75, 1)
        G.window.rotation = (-45, -45)
        size = G.window.get_size()
        self.label1.position = (size[0] / 2, size[1] / 2)
        G.window.set_exclusive_mouse(False)

    def on_event(self, name, *args, **kwargs):
        if name == "update":
            self.timer += args[0]
            if self.timer > ITEM_GEN_TIME:
                self.timer -= ITEM_GEN_TIME
                # blockitemfactory.close()
                blockitemfactory.step()
        elif name == "draw_3d_start":
            pyglet.gl.glClearColor(1.0, 1.0, 1.0, 0.0)
        elif name == "draw_2d_end":
            if blockitemfactory.closed:
                self.label1.draw()
                blockitemfactory.close_M()


dummyinventoryblockitemfactory = DummyInventoryBlockItemFactory()

