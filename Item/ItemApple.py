import globals as G
import Item.IItem


@G.itemhandler
class ItemApple(Item.IItem.IItem):
    @staticmethod
    def getName():
        return "minecraft:apple"

    def getItemFile(self):
        return G.local + "/assets/textures/item/apple.png"

    @staticmethod
    def has_block():
        return False
