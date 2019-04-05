import globals as G
import gui.Inventory
import gui.player.hotbar
import gui.player.IPlayerInventoryMode


class PlayerInventory(gui.Inventory.Inventory):
    # a name -> None / <Inventory> dict for the states of the inventory
    # todo: add creative_inventory, spectator_inventory, spectator_hotbar, creative tab injection
    POSSIBLE_MODES = {"hotbar": gui.player.hotbar.Hotbar(),  # not implemented
                      "inventory": None}  # not implemented

    def __init__(self, player):

        self.mode_inv = None

        self.__mode = None
        self.set_mode("hotbar")

        self.player = player

        # self.bgimage = pyglet.sprite.Sprite(pyglet.image.load(G.local+"/tmp/gui/player/main.png"))

        size = G.window.get_size()

        self.init((size[0]/2-176/2, size[1]/2-166/2))
        for inv in self.POSSIBLE_MODES.values():
            if inv and issubclass(type(inv), gui.player.IPlayerInventoryMode.IPlayerInventoryMode):
                inv.set_position(self.position)

    def draw_background(self):
        # self.bgimage.draw()
        pass

    def on_event(self, name, *args, **kwargs):
        pass

    def should_be_closed_by_esc(self):
        if not self.__mode:
            self.set_mode("hotbar")
        return self.__mode != "hotbar"

    def should_game_freeze(self):
        return self.should_be_closed_by_esc()

    def is_blocking_interaction(self):
        return self.should_be_closed_by_esc()

    def on_close(self):
        self.set_mode("hotbar")
        G.inventoryhandler.show_inventory(self)

    def set_mode(self, mode):
        self.__mode = mode
        if mode not in self.POSSIBLE_MODES: raise ValueError("unsupported player inventory mode: '"+str(mode)+"'")
        inv = self.POSSIBLE_MODES[mode]
        if self.mode_inv and self.mode_inv != "hotbar":
            if type(self.mode_inv) == list:
                [G.inventoryhandler.hide_inventory(x) for x in self.mode_inv]
            else:
                G.inventoryhandler.hide_inventory(self.mode_inv)

        if not inv: return
        if type(inv) == list:
            [G.inventoryhandler.show_inventory(x) for x in inv]
            [[G.inventoryhandler.show_inventory(x) for x in a.get_depend_inventory_parts()] for a in inv]
        else:
            G.inventoryhandler.show_inventory(inv)
            [G.inventoryhandler.show_inventory(x) for x in inv.get_depend_inventory_parts()]
        self.mode_inv = inv

    def get_mode(self): return self.__mode

