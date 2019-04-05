import globals as G
import pyglet
import Item.IItem


class ItemStack:
    def __init__(self, item_or_name_or_itemfile, amount):
        if item_or_name_or_itemfile in G.itemhandler.itemnametofile:
            self.itemfile = G.itemhandler.itemnametofile[item_or_name_or_itemfile]
            self.item = None
        elif item_or_name_or_itemfile in G.itemhandler.itemnametofile.values():
            self.itemfile = item_or_name_or_itemfile
            self.item = None
        elif type(item_or_name_or_itemfile) == Item.IItem.IItem:
            self.itemfile = item_or_name_or_itemfile.getItemFile()
            self.item = item_or_name_or_itemfile
        try:
            if issubclass(item_or_name_or_itemfile, Item.IItem.IItem):
                self.item = item_or_name_or_itemfile()
                self.itemfile = self.item.getName()
        except:
            pass
        raise NotImplementedError("ItemStack system not fully implemented")

    def set_amount(self, amount):
        self.amount = amount

