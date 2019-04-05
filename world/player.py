import globals as G
import gui.PlayerInventory
import texture.BlockItemFactory


class Player:
    def __init__(self):
        self.playerinventory = gui.PlayerInventory.PlayerInventory(self)
        G.inventoryhandler.show_inventory(texture.BlockItemFactory.dummyinventoryblockitemfactory)
        # G.inventoryhandler.show_inventory(self.playerinventory)

