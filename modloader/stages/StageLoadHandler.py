import globals as G
import gui.Inventory
import pyglet
import TickHandler


class DummyInventoryStageLoadHandler(gui.Inventory.IInventoryBlocking):
    def __init__(self):
        self.init((0, 0))

    def on_open(self):
        G.window.position = (1, 0.75, 1)
        G.window.rotation = (-45, -45)
        size = G.window.get_size()
        G.window.set_exclusive_mouse(False)

    def on_event(self, name, *args, **kwargs):
        if name == "draw_3d_start":
            pyglet.gl.glClearColor(1.0, 1.0, 1.0, 0.0)
        elif name == "draw_2d_end":
            # print("drawing", G.stageloadhandler.stages, G.stageloadhandler.activestage)
            if 0 <= G.stageloadhandler.activestage < len(G.stageloadhandler.stages):
                G.stageloadhandler.stages[G.stageloadhandler.activestage].draw()


class StageLoadHandler:
    def __init__(self):
        self.activestage = -1
        self.stages = []
        self.dummystageloadhandlerinventory = None

    def add_stage(self, stage):
        stage.sublevel = 1
        self.stages.append(stage)

    def startup(self):
        self.dummystageloadhandlerinventory = DummyInventoryStageLoadHandler()
        G.inventoryhandler.show_inventory(self.dummystageloadhandlerinventory)
        TickHandler.handler.tick_function(self.next_stage, 10)

    def next_stage(self):
        if self.activestage == -1:
            self.activestage += 1
            TickHandler.handler.tick_function(self.next_stage, 1)
            return
        if self.stages[self.activestage].step():
            self.activestage += 1
        if self.activestage >= len(self.stages):
            print("closing stage system")
            pyglet.gl.glClearColor(0.5, 0.69, 1.0, 1)
            G.player.setup()
            import texture.BlockItemFactory
            G.inventoryhandler.show_inventory(texture.BlockItemFactory.dummyinventoryblockitemfactory)
            return
        TickHandler.handler.tick_function(self.next_stage, 1)


G.stageloadhandler = StageLoadHandler()

