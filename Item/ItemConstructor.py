import globals as G
import Item.IItem


class ItemConstructor:
    def __init__(self):
        pass

    def construct_item(self, name, itemfile=G.local+"/tmp/missing_texture.png", has_block=False):
        @G.itemhandler
        class ConstructedItem(Item.IItem.IItem):
            @staticmethod
            def getName():
                return name

            def getItemFile(self):
                return itemfile

            @staticmethod
            def has_block():
                return has_block


G.itemconstructor = ItemConstructor()


G.itemconstructor.construct_item("minecraft:apple", G.local + "/assets/textures/item/apple.png")
G.itemconstructor.construct_item("minecraft:stick", G.local + "/assets/textures/item/stick.png")
G.itemconstructor.construct_item("minecraft:book", G.local + "/assets/textures/item/book.png")
G.itemconstructor.construct_item("minecraft:enchanted_book", G.local + "/assets/textures/item/enchanted_book.png")
G.itemconstructor.construct_item("minecraft:coal", G.local + "/assets/textures/item/coal.png")
G.itemconstructor.construct_item("minecraft:diamond", G.local + "/assets/textures/item/diamond.png")
G.itemconstructor.construct_item("minecraft:redstone", G.local + "/assets/textures/item/redstone.png")
G.itemconstructor.construct_item("minecraft:quartz", G.local + "/assets/textures/item/quartz.png")
G.itemconstructor.construct_item("minecraft:iron_ingot", G.local + "/assets/textures/item/iron_ingot.png")
G.itemconstructor.construct_item("minecraft:gold_ingot", G.local + "/assets/textures/item/gold_ingot.png")
G.itemconstructor.construct_item("minecraft:emerald", G.local + "/assets/textures/item/emerald.png")
G.itemconstructor.construct_item("minecraft:lapis_lazuli", G.local + "/assets/textures/item/lapis_lazuli.png")

