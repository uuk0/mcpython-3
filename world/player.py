import globals as G
import gui.PlayerInventory
import texture.BlockItemFactory
import chat.command.CommandParser
import chat.command.CommandHandler
import chat.Chat
import gui.ItemStack


class Player:
    def __init__(self):
        G.player = self
        G.worldaccess.create_dimension_from_id(0)  # Overworld
        self.dimension = 0
        self.gamemode = 0
        self.playerinventory = None
        self.selectedinventoryslot = 0
        self.chat = chat.Chat.Chat()

    def setup(self):
        self.playerinventory = gui.PlayerInventory.PlayerInventory(self)

    def kill(self):
        G.commandparser.parse_command("/clear")
        if (0, 0) not in G.worldaccess.get_active_dimension_access().worldgenerationprovider.highmap.map:
            G.window.position = (0, 100000, 0)
        else:
            G.window.position = (0, G.worldaccess.get_active_dimension_access().
                                 worldgenerationprovider.highmap[(0, 0)][-1][1]+2, 0)

    def set_gamemode(self, gamemode):
        if gamemode == self.gamemode:
            return
        if gamemode in [0, 2]:
            G.window.flying = False
        elif gamemode == 3:
            G.window.flying = True
        self.gamemode = gamemode

    def add_block_drop_to_inventory(self, iblock):
        drops = iblock.get_drop(gui.ItemStack.ItemStack.empty())
        for element in drops.keys():
            self.add_to_free_place(element, drops[element])

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
            if amount <= 0:
                return
        basestack = gui.ItemStack.ItemStack(itemname, 1)
        maxsize = 64 if not basestack.item else basestack.item.getMaxStackSize()
        while amount > 0:
            vstack = gui.ItemStack.ItemStack(itemname, amount if amount < maxsize else maxsize)
            amount -= maxsize
            flag = True
            for slot in slots:
                if not slot.get_stack().itemfile and flag:
                    slot.set_stack(vstack)
                    flag = False
            if flag:
                print("can't find an slot that is free")
                return

