import globals as G
import gui.Inventory
import gui.player.IPlayerInventoryMode
import gui.Slot
import pyglet.window.key, pyglet.window.mouse
import gui.ItemStack
import modloader.events.LoadStageEvent


@modloader.events.LoadStageEvent.playerinventory_load("minecraft")
def setup_player_inventory(*args):
    import gui.player.hotbar
    import gui.player.main

    hotbar = gui.player.hotbar.Hotbar()
    main = gui.player.main.Main(hotbar)

    PlayerInventory.POSSIBLE_MODES["hotbar"] = hotbar
    PlayerInventory.POSSIBLE_MODES["inventory"] = main


class PlayerInventory(gui.Inventory.Inventory):
    # a name -> None / <Inventory> dict for the states of the inventory
    # todo: add creative_inventory, spectator_inventory, spectator_hotbar, creative tab injection
    POSSIBLE_MODES = {}

    def __init__(self, player):

        self.mouse_position = (0, 0)

        self.mode_inv = None

        self.__mode = None

        self.player = player

        # self.bgimage = pyglet.sprite.Sprite(pyglet.image.load(G.local+"/tmp/gui/player/main.png"))
        # -> part of main image

        size = G.window.get_size()

        self.init((size[0]/2, size[1]/2))

        self.set_mode("hotbar")

        for inv in self.POSSIBLE_MODES.values():
            if inv and issubclass(type(inv), gui.player.IPlayerInventoryMode.IPlayerInventoryMode):
                inv.set_position(self.position)

    def create_slots(self):
        return [gui.Slot.Slot()] # moving slot

    def draw_background(self):
        pass

    def on_event(self, name, *args, **kwargs):
        if name == "on_resize":
            for inv in self.POSSIBLE_MODES.values():
                if inv and issubclass(type(inv), gui.player.IPlayerInventoryMode.IPlayerInventoryMode):
                    inv.set_position([args[0]/2, args[1]/2])
        elif name == "on_mouse_press":
            # handle mouse input
            mslot = self.slots[0]
            hslot = self.get_slot(*args[:2])
            if not hslot:  # test for other interfaces
                pass
            if args[2] == pyglet.window.mouse.LEFT:
                if hslot:
                    if mslot.get_stack().is_empty():
                        mslot.position = self.mouse_position
                        mslot.set_stack(hslot.get_stack())
                        hslot.set_stack(gui.ItemStack.ItemStack.empty())
                    elif hslot.is_player_interaction_allowed():
                        if hslot.get_stack().is_empty():
                            b = hslot.set_stack(mslot.get_stack())
                            if b:
                                mslot.set_stack(gui.ItemStack.ItemStack.empty())
                        else:
                            stack = hslot.get_stack()
                            b = hslot.set_stack(mslot.get_stack())
                            if b:
                                mslot.set_stack(stack)
            elif args[2] == pyglet.window.mouse.RIGHT:
                if mslot.get_stack().is_empty():
                    if not hslot.get_stack().is_empty():
                        amh = hslot.get_stack().amount
                        v1 = round(amh / 2)
                        v2 = amh - v1
                        mslot.set_stack(gui.ItemStack.ItemStack(hslot.get_stack().itemname, v2))
                        hslot.get_stack().amount = v1
                elif hslot.is_player_interaction_allowed():
                    if hslot.get_stack().is_empty():
                        hslot.set_stack(gui.ItemStack.ItemStack(mslot.get_stack().itemname, 1))
                        mslot.get_stack().amount -= 1
                    elif hslot.get_stack().itemname == mslot.get_stack().itemname:
                        hslot.get_stack().amount += 1
                        mslot.get_stack().amount -= 1
            elif args[2] == pyglet.window.mouse.MIDDLE:
                if mslot.stack.is_empty():
                    mslot.position = self.mouse_position
                    mslot.set_stack(gui.ItemStack.ItemStack(hslot.get_stack().itemname,
                                                            64 if not hslot.get_stack().item else
                                                            hslot.get_stack().item.getMaxStackSize()))
                else:
                    if hslot.get_stack().is_empty():
                        hslot.set_stack(gui.ItemStack.ItemStack(mslot.stack.itemname, 1))
                        mslot.stack.amount -= 1
                        if mslot.stack.amount == 0:
                            mslot.set_stack(gui.ItemStack.ItemStack.empty())
        elif name == "on_mouse_motion":  # only used when in special mode
            self.mouse_position = args[:2]
            mslot = self.slots[0]
            if not mslot.stack.is_empty():
                mslot.position = args[:2]
        elif name == "on_key_press":
            slot = self.get_slot(*self.mouse_position)
            if slot:
                if args[0] in G.window.num_keys:
                    index = (args[0] - G.window.num_keys[0])
                    rslot = self.POSSIBLE_MODES["hotbar"].slots[index]
                    if rslot:
                        if rslot.stack.is_empty():
                            rslot.set_stack(slot.get_stack())
                            slot.set_stack(gui.ItemStack.ItemStack.empty())
                        else:
                            tstack = slot.get_stack()
                            slot.set_stack(rslot.get_stack())
                            rslot.set_stack(tstack)

    def get_all_active_slots(self):
        slots = []
        for inventory in G.inventoryhandler.visable_inventorys:
            slots += inventory.get_setable_slots()
        return slots

    def get_slot(self, x, y):
        slots = self.get_all_active_slots()
        for slot in slots:
            px, py = slot.position
            if x >= px >= x - 32 and y >= py >= y - 32:
                return slot

    def should_be_closed_by_esc(self):
        return False

    def should_game_freeze(self):
        return self.should_be_closed_by_esc()

    def is_blocking_interaction(self):
        return self.should_be_closed_by_esc()

    def on_close(self):
        self.set_mode("hotbar")
        G.inventoryhandler.overlaydraw.remove(self)
        G.inventoryhandler.show_inventory(self)

    def set_mode(self, mode):
        self.__mode = mode
        if mode not in self.POSSIBLE_MODES: raise ValueError("unsupported player inventory mode: '"+str(mode)+"'")
        inv = self.POSSIBLE_MODES[mode]
        if self.mode_inv:
            if type(self.mode_inv) == list:
                [G.inventoryhandler.hide_inventory(x) for x in self.mode_inv]
            elif type(self.mode_inv) != gui.player.hotbar.Hotbar:
                G.inventoryhandler.hide_inventory(self.mode_inv)

        if not inv: return
        if type(inv) == list:
            [G.inventoryhandler.show_inventory(x) for x in inv]
            [[G.inventoryhandler.show_inventory(x) for x in a.get_depend_inventory_parts()] for a in inv]
        else:
            G.inventoryhandler.show_inventory(inv)
            [G.inventoryhandler.show_inventory(x) for x in inv.get_depend_inventory_parts()]
        self.mode_inv = inv
        if mode == "hotbar":
            stack = self.slots[0].get_stack()
            if not stack.is_empty():
                G.player.add_to_free_place(stack.itemname, stack.amount)
                self.slots[0].set_stack(gui.ItemStack.ItemStack.empty())

    def get_mode(self): return self.__mode

    def get_setable_slots(self): return []

    def on_open(self):
        G.inventoryhandler.overlaydraw.append(self)

    def overlay_draw(self):
        self.draw_background()
        for slot in self.slots:
            slot.draw()
        self.draw_overlay()

    def draw(self): pass


