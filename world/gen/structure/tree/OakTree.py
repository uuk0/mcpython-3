import globals as G
import world.gen.structure.tree.ITreeStructure


class OakTree(world.gen.structure.tree.ITreeStructure.ITreeStructure):
    def __init__(self, chance):
        self.chance = chance

    @staticmethod
    def getLogBlock():
        return "minecraft:oak_log"

    @staticmethod
    def getHighRange():
        return [4, 7]

    @staticmethod
    def getLeaveBlock():
        return "minecraft:oak_leaves"

    def getStructureGenerationChance(self) -> int:
        return self.chance


oaktreeplains = OakTree(1/200)

