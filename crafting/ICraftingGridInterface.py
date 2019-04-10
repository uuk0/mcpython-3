import globals as G
import crafting.CraftingInterface


class ICraftingInterface(crafting.CraftingInterface):
    def __init__(self, inventory):
        self.inventory = inventory

    @staticmethod
    def getRecipeTypeName(): return "crafting"

    def getRecipeGridNames(self):
        grids = []
        size = self.getMaxGridSize()
        for x in range(size[0]):
            for y in range(size[1]):
                grids.append(str(x)+"x"+str(y))
        if self.allow_shapless(): grids.append("shapeless")
        return grids

    @staticmethod
    def getMaxGridSize():
        raise NotImplementedError()

    def update_recipe(self, slot):
        if slot in self.getInputSlots():
            pass
        elif slot in self.getMaxGridSize():
            pass
        else:
            raise RuntimeError()

    @staticmethod
    def allow_shapless(): return True

