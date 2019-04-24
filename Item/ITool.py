import globals as G
import Item.IItem


class ToolClass:
    def __init__(self, name, extends=[]):
        self.name = name
        self.extends = extends
        self.childs = []
        for toolclass in extends:
            toolclass.childs.append(self)

    def contains_type(self, type):
        return type == self or any([toolclass.contains_type(type) for toolclass in self.childs])


shovel = ToolClass("shovel")
axe = ToolClass("axe")
pickaxe = ToolClass("pickaxe")
sword = ToolClass("sword")
hoe = ToolClass("hoe")


class ITool(Item.IItem.IItem):
    @staticmethod
    def get_tool_types():
        return []

    def get_tool_level(self):
        return 0

    def get_max_durability(self):
        return 0

    def getMaxStackSize(self):
        return 1

