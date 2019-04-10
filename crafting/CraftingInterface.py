"""
an interface between an Inventory and the representing RecipeType
"""
import globals as G


class CraftingInterface:

    @staticmethod
    def getRecipeTypeName(): raise NotImplementedError()

    @staticmethod
    def getRecipeGridNames(): return []

    def update(self, slot):
        """
        call these function in order to update the whole thing
        :param slot: the slot that has been updated
        """
        recipetype = G.craftinghandler.recipetypes[self.getRecipeTypeName()]
        if slot in self.getInputSlots():
            if not recipetype.preconsuming:
                self.update_recipe(slot)
        elif slot in self.getOutputSlots():
            if not recipetype.outputinputautoremoving:
                self.update_recipe(slot)
        elif slot in self.getByPassSlots():
            if not recipetype.preconsuming:
                self.update_recipe(slot)
        else:
            raise RuntimeError("slot is not mentioned by interface")

    def getInputSlots(self): return []

    def getOutputSlots(self): return []

    def getByPassSlots(self): return []

    def update_recipe(self, slot):
        raise NotImplementedError()

