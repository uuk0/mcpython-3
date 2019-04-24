import globals as G
import Item.IItem


@G.itemhandler
class EnchantedBook(Item.IItem.IItem):
    def __init__(self):
        Item.IItem.IItem.__init__(self)

    @staticmethod
    def getName():
        return "minecraft:enchanted_book"

    def getItemFile(self):
        return G.local + "/assets/textures/item/enchanted_book.png"

    def getMaxStackSize(self):
        return 1

    @staticmethod
    def has_block():
        return False

