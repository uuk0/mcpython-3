import globals as G
import Item.IItem
import modloader.events.LoadStageEvent
import Item.ITool


class ItemConstructor:
    def __init__(self):
        pass

    def construct_item(self, name, itemfile=G.local+"/tmp/missing_texture.png", has_block=False,
                       toolgroups=[], toollevel=0, duribility=0):
        @modloader.events.LoadStageEvent.items("minecraft", action="loading item "+str(name),
                                                    arguments=[name, itemfile, has_block, toolgroups, toollevel,
                                                               duribility])
        def load_item(eventname, itemname, itemfilepath, hasblock, toolgroupsnot, toollevelinfo,
                      duribilityinfo):
            @G.itemhandler
            class ConstructedItem(Item.IItem.IItem if len(toolgroupsnot) == 0 else Item.ITool.ITool):
                @staticmethod
                def getName():
                    return itemname

                def getItemFile(self):
                    return itemfilepath

                @staticmethod
                def has_block():
                    return hasblock

                @staticmethod
                def get_tool_types():
                    return toolgroupsnot

                def get_tool_level(self):
                    return toollevelinfo

                def get_max_durability(self):
                    return duribilityinfo


G.itemconstructor = ItemConstructor()


def load_models():

    # normal items

    G.itemconstructor.construct_item("minecraft:apple", G.local + "/assets/textures/item/apple.png")
    G.itemconstructor.construct_item("minecraft:stick", G.local + "/assets/textures/item/stick.png")
    G.itemconstructor.construct_item("minecraft:book", G.local + "/assets/textures/item/book.png")
    # G.itemconstructor.construct_item("minecraft:enchanted_book", G.local + "/assets/textures/item/enchanted_book.png")
    G.itemconstructor.construct_item("minecraft:coal", G.local + "/assets/textures/item/coal.png")
    G.itemconstructor.construct_item("minecraft:diamond", G.local + "/assets/textures/item/diamond.png")
    G.itemconstructor.construct_item("minecraft:redstone", G.local + "/assets/textures/item/redstone.png")
    G.itemconstructor.construct_item("minecraft:quartz", G.local + "/assets/textures/item/quartz.png")
    G.itemconstructor.construct_item("minecraft:iron_ingot", G.local + "/assets/textures/item/iron_ingot.png")
    G.itemconstructor.construct_item("minecraft:gold_ingot", G.local + "/assets/textures/item/gold_ingot.png")
    G.itemconstructor.construct_item("minecraft:emerald", G.local + "/assets/textures/item/emerald.png")
    G.itemconstructor.construct_item("minecraft:lapis_lazuli", G.local + "/assets/textures/item/lapis_lazuli.png")
    G.itemconstructor.construct_item("minecraft:seed", G.local+"/assets/textures/item/wheat_seeds.png")
    G.itemconstructor.construct_item("minecraft:snow", G.local + "/assets/textures/item/snowball.png")

    # tools
    G.itemconstructor.construct_item("minecraft:wood_shovel", G.local + "/assets/textures/item/wooden_shovel.png",
                                     toolgroups=[Item.ITool.shovel], toollevel=1, duribility=60)
    G.itemconstructor.construct_item("minecraft:stone_shovel", G.local + "/assets/textures/item/stone_shovel.png",
                                     toolgroups=[Item.ITool.shovel], toollevel=2, duribility=132)
    G.itemconstructor.construct_item("minecraft:iron_shovel", G.local + "/assets/textures/item/iron_shovel.png",
                                     toolgroups=[Item.ITool.shovel], toollevel=3, duribility=251)
    G.itemconstructor.construct_item("minecraft:golden_shovel", G.local + "/assets/textures/item/golden_shovel.png",
                                     toolgroups=[Item.ITool.shovel], toollevel=4, duribility=33)
    G.itemconstructor.construct_item("minecraft:diamond_shovel", G.local + "/assets/textures/item/diamond_shovel.png",
                                     toolgroups=[Item.ITool.shovel], toollevel=5, duribility=1562)

    G.itemconstructor.construct_item("minecraft:wood_axe", G.local + "/assets/textures/item/wooden_axe.png",
                                     toolgroups=[Item.ITool.axe], toollevel=1, duribility=60)
    G.itemconstructor.construct_item("minecraft:stone_axe", G.local + "/assets/textures/item/stone_axe.png",
                                     toolgroups=[Item.ITool.axe], toollevel=2, duribility=132)
    G.itemconstructor.construct_item("minecraft:iron_axe", G.local + "/assets/textures/item/iron_axe.png",
                                     toolgroups=[Item.ITool.axe], toollevel=3, duribility=251)
    G.itemconstructor.construct_item("minecraft:golden_axe", G.local + "/assets/textures/item/golden_axe.png",
                                     toolgroups=[Item.ITool.axe], toollevel=4, duribility=33)
    G.itemconstructor.construct_item("minecraft:diamond_axe", G.local + "/assets/textures/item/diamond_axe.png",
                                     toolgroups=[Item.ITool.axe], toollevel=5, duribility=1562)

    G.itemconstructor.construct_item("minecraft:wood_pickaxe", G.local + "/assets/textures/item/wooden_pickaxe.png",
                                     toolgroups=[Item.ITool.pickaxe], toollevel=1, duribility=60)
    G.itemconstructor.construct_item("minecraft:stone_pickaxe", G.local + "/assets/textures/item/stone_pickaxe.png",
                                     toolgroups=[Item.ITool.pickaxe], toollevel=2, duribility=132)
    G.itemconstructor.construct_item("minecraft:iron_pickaxe", G.local + "/assets/textures/item/iron_pickaxe.png",
                                     toolgroups=[Item.ITool.pickaxe], toollevel=3, duribility=251)
    G.itemconstructor.construct_item("minecraft:golden_pickaxe", G.local + "/assets/textures/item/golden_pickaxe.png",
                                     toolgroups=[Item.ITool.pickaxe], toollevel=4, duribility=33)
    G.itemconstructor.construct_item("minecraft:diamond_pickaxe", G.local + "/assets/textures/item/diamond_pickaxe.png",
                                     toolgroups=[Item.ITool.pickaxe], toollevel=5, duribility=1562)

    G.itemconstructor.construct_item("minecraft:wood_sword", G.local + "/assets/textures/item/wooden_sword.png",
                                     toolgroups=[Item.ITool.sword], toollevel=1, duribility=60)
    G.itemconstructor.construct_item("minecraft:stone_sword", G.local + "/assets/textures/item/stone_sword.png",
                                     toolgroups=[Item.ITool.sword], toollevel=2, duribility=132)
    G.itemconstructor.construct_item("minecraft:iron_sword", G.local + "/assets/textures/item/iron_sword.png",
                                     toolgroups=[Item.ITool.sword], toollevel=3, duribility=251)
    G.itemconstructor.construct_item("minecraft:golden_sword", G.local + "/assets/textures/item/golden_sword.png",
                                     toolgroups=[Item.ITool.sword], toollevel=4, duribility=33)
    G.itemconstructor.construct_item("minecraft:diamond_sword", G.local + "/assets/textures/item/diamond_sword.png",
                                     toolgroups=[Item.ITool.sword], toollevel=5, duribility=1562)

    G.itemconstructor.construct_item("minecraft:wood_hoe", G.local + "/assets/textures/item/wooden_hoe.png",
                                     toolgroups=[Item.ITool.hoe], toollevel=1, duribility=60)
    G.itemconstructor.construct_item("minecraft:stone_hoe", G.local + "/assets/textures/item/stone_hoe.png",
                                     toolgroups=[Item.ITool.hoe], toollevel=2, duribility=132)
    G.itemconstructor.construct_item("minecraft:iron_hoe", G.local + "/assets/textures/item/iron_hoe.png",
                                     toolgroups=[Item.ITool.hoe], toollevel=3, duribility=251)
    G.itemconstructor.construct_item("minecraft:golden_hoe", G.local + "/assets/textures/item/golden_hoe.png",
                                     toolgroups=[Item.ITool.hoe], toollevel=4, duribility=33)
    G.itemconstructor.construct_item("minecraft:diamond_hoe", G.local + "/assets/textures/item/diamond_hoe.png",
                                     toolgroups=[Item.ITool.hoe], toollevel=5, duribility=1562)

    # plants
    G.itemconstructor.construct_item("minecraft:sugar_cane", G.local + "/assets/textures/item/sugar_cane.png",
                                     has_block=True)
    G.itemconstructor.construct_item("minecraft:allium", G.local + "/assets/textures/block/allium.png",
                                     has_block=True)
    G.itemconstructor.construct_item("minecraft:azure_bluet", G.local + "/assets/textures/block/azure_bluet.png",
                                     has_block=True)
    G.itemconstructor.construct_item("minecraft:blue_orchid", G.local + "/assets/textures/block/blue_orchid.png",
                                     has_block=True)
    G.itemconstructor.construct_item("minecraft:cornflower", G.local + "/assets/textures/block/cornflower.png",
                                     has_block=True)
    G.itemconstructor.construct_item("minecraft:dandelion", G.local + "/assets/textures/block/dandelion.png",
                                     has_block=True)
    G.itemconstructor.construct_item("minecraft:grass_small", G.local + "/tmp/blocks/grass_small.png",
                                     has_block=True)
    G.itemconstructor.construct_item("minecraft:lilac", G.local + "/assets/textures/block/lilac_top.png",
                                     has_block=True)
    G.itemconstructor.construct_item("minecraft:lily_of_the_valley",
                                     G.local + "/assets/textures/block/lily_of_the_valley.png", has_block=True)
    G.itemconstructor.construct_item("minecraft:orange_tulip", G.local + "/assets/textures/block/orange_tulip.png",
                                     has_block=True)
    G.itemconstructor.construct_item("minecraft:oxeye_daisy", G.local + "/assets/textures/block/oxeye_daisy.png",
                                     has_block=True)
    G.itemconstructor.construct_item("minecraft:peony", G.local + "/assets/textures/block/peony_top.png",
                                     has_block=True)
    G.itemconstructor.construct_item("minecraft:pink_tulip", G.local + "/assets/textures/block/pink_tulip.png",
                                     has_block=True)
    G.itemconstructor.construct_item("minecraft:poppy", G.local + "/assets/textures/block/poppy.png",
                                     has_block=True)
    G.itemconstructor.construct_item("minecraft:red_tulip", G.local + "/assets/textures/block/red_tulip.png",
                                     has_block=True)
    G.itemconstructor.construct_item("minecraft:rose_bush", G.local + "/assets/textures/block/rose_bush_top.png",
                                     has_block=True)
    G.itemconstructor.construct_item("minecraft:white_tulip", G.local + "/assets/textures/block/white_tulip.png",
                                     has_block=True)
    G.itemconstructor.construct_item("minecraft:wither_rose", G.local + "/assets/textures/block/wither_rose.png",
                                     has_block=True)
    G.itemconstructor.construct_item("minecraft:oak_sapling", G.local + "/assets/textures/block/oak_sapling.png",
                                     has_block=True)


load_models()

