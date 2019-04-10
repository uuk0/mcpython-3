import globals as G
import crafting.CraftingInterface
import crafting.ICraftingGridInterface


class InventoryCrafting(crafting.ICraftingGridInterface.ICraftingInterface):
    @staticmethod
    def getRecipeTypeName(): return "crafting"

    def getInputSlots(self):
        return self.inventory.slots[:4]

    def getOutputSlots(self): return [self.inventory.slots[4]]

    @staticmethod
    def getMaxGridSize():
        return 2, 2

