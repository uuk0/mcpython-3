import globals as G
import gui.PlayerInventory
import texture.BlockItemFactory
import chat.Chat
import gui.ItemStack
import util.vector


class Player:
    def __init__(self):
        self.chat = chat.Chat.Chat()
        G.player = self
        self.playerinventory = gui.PlayerInventory.PlayerInventory(self)
        G.inventoryhandler.show_inventory(texture.BlockItemFactory.dummyinventoryblockitemfactory)
        self.selectedinventoryslot = 0
        self.gamemode = 0

    def add_to_free_place(self, itemname, amount=1):
        slots = G.player.playerinventory.POSSIBLE_MODES["hotbar"].slots + \
                G.player.playerinventory.POSSIBLE_MODES["inventory"].slots[9:]
        first_empty = None
        for slot in slots:
            itemstack = slot.get_stack()
            if not itemstack.is_empty():
                if itemstack.itemname == itemname:
                    if (itemstack.item and itemstack.item.getMaxStackSize() >= amount + itemstack.amount) or \
                            (not itemstack.item and 64 >= amount + itemstack.amount):
                        itemstack.amount += amount
                        return
                    else:
                        m = itemstack.item.getMaxStackSize() if itemstack.item else 64
                        amount = amount - (m - itemstack.amount)
                        itemstack.amount = m
        vstack = gui.ItemStack.ItemStack(itemname, amount)
        for slot in slots:
            if slot.set_stack(vstack):
                return
        print("can't find an slot that is free")

    def set_gamemode(self, gamemode):
        if gamemode == self.gamemode: return
        if gamemode in [0, 2]:
            G.window.flying = False
        elif gamemode == 3:
            G.window.flying = True
        self.gamemode = gamemode

    def kill(self):
        G.commandparser.parse_command("/clear")

