import globals as G
import Item.IItem


@G.itemhandler
class ItemStick(Item.IItem.IItem):
    @staticmethod
    def getName():
        return "minecraft:stick"

    def getItemFile(self):
        return G.local + "/assets/textures/item/stick.png"

    @staticmethod
    def has_block():
        return False
