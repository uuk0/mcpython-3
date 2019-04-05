import globals as G


class InventoryHandler:
    def __init__(self):
        self.inventorys = []
        self.visable_inventorys = []

    def draw(self):
        if texture.BlockItemFactory.dummyinventoryblockitemfactory in self.visable_inventorys: return
        for inventory in self.visable_inventorys:
            inventory.draw()

    def add_inventory(self, inventory):
        self.inventorys.append(inventory)

    def remove_inventory(self, inventory):
        self.inventorys.remove(inventory)
        if inventory in self.visable_inventorys: self.hide_inventory(inventory)

    def show_inventory(self, inventory):
        if inventory in self.visable_inventorys: return
        inventory.on_open()
        self.visable_inventorys.append(inventory)
        if inventory.should_activate_mouse():
            G.window.set_exclusive_mouse(False)
            G.window.strafe = [0, 0]
            G.window.is_pressing_space = False

    def hide_inventory(self, inventory):
        if inventory not in self.visable_inventorys: return
        inventory.on_close()
        self.visable_inventorys.remove(inventory)

    def should_game_freeze(self):
        for inventory in self.visable_inventorys:
            if inventory.is_blocking_interaction():
                return True

    def send_event(self, name, *args, **kwargs):
        for inventory in self.visable_inventorys:
            inventory.on_event(name, *args, **kwargs)

    def remove_last_inventory_from_stack(self):
        for inventory in self.visable_inventorys[:]:
            # print(inventory, inventory.should_be_closed_by_esc())
            if inventory.should_be_closed_by_esc():
                self.hide_inventory(inventory)
                if inventory.is_only_esc_closed():
                    return
        G.window.set_exclusive_mouse(True)


G.inventoryhandler = handler = InventoryHandler()


import texture.BlockItemFactory

