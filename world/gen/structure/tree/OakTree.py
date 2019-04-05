import globals as G
import world.gen.structure.tree.ITreeStructure


class OakTree(world.gen.structure.tree.ITreeStructure.ITreeStructure):
    @staticmethod
    def getLogBlock():
        return "minecraft:oak_log"

    @staticmethod
    def getHighRange():
        return [4, 7]

    @staticmethod
    def getLeaveBlock():
        return "minecraft:oak_leaves"


oaktree = OakTree()

