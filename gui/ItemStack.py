import globals as G
import pyglet
import Item.IItem
import Item.ItemHandler
import texture.BlockItemFactory


class ItemStack:
    def __init__(self, item_or_name_or_itemfile, amount):
        flag = False
        if not item_or_name_or_itemfile:
            self.itemfile = None
            self.item = None
            self.itemname = None
        elif item_or_name_or_itemfile in G.itemhandler.itemnametofile:
            self.itemfile = G.itemhandler.itemnametofile[item_or_name_or_itemfile]
            self.item = None
            self.itemname = item_or_name_or_itemfile
        elif item_or_name_or_itemfile in G.itemhandler.itemnametofile.values():
            self.itemfile = item_or_name_or_itemfile
            self.item = None
            self.itemname = None
        elif type(item_or_name_or_itemfile) == Item.IItem.IItem:
            self.itemfile = item_or_name_or_itemfile.getItemFile()
            self.item = item_or_name_or_itemfile
            self.itemname = self.item.getBlockName()
        else:
            flag = True
        try:
            if issubclass(item_or_name_or_itemfile, Item.IItem.IItem) and flag:
                self.item = item_or_name_or_itemfile()
                self.itemfile = self.item.getName()
                flag = False
                self.itemname = self.item.getBlockName()
        except:
            pass
        if flag:
            raise NotImplementedError("ItemStack system not fully implemented")
        self.amount = amount

    def set_amount(self, amount):
        self.amount = amount

    def is_empty(self):
        return not self.itemfile

    def set_item(self, item_or_name_or_itemfile):
        flag = False
        if not item_or_name_or_itemfile:
            self.itemfile = None
            self.item = None
            self.itemname = None
        elif item_or_name_or_itemfile in G.itemhandler.itemnametofile:
            self.itemfile = G.itemhandler.itemnametofile[item_or_name_or_itemfile]
            self.item = None
            self.itemname = item_or_name_or_itemfile
        elif item_or_name_or_itemfile in G.itemhandler.itemnametofile.values():
            self.itemfile = item_or_name_or_itemfile
            self.item = None
            self.itemname = None
        elif type(item_or_name_or_itemfile) == Item.IItem.IItem:
            self.itemfile = item_or_name_or_itemfile.getItemFile()
            self.item = item_or_name_or_itemfile
            self.itemname = self.item.getBlockName()
        else:
            flag = True
        try:
            if issubclass(item_or_name_or_itemfile, Item.IItem.IItem) and flag:
                self.item = item_or_name_or_itemfile()
                self.itemfile = self.item.getName()
                flag = False
                self.itemname = self.item.getBlockName()
        except:
            pass
        if flag:
            raise NotImplementedError("ItemStack system not fully implemented")

    @staticmethod
    def empty():
        return ItemStack(None, 0)
