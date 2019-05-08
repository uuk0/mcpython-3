"""
an system bound to IRecipeProviders to deal with items in an inventory an checking for recipes
"""

import gui.Slot
import gui.ItemStack
import gui.Inventory
import crafting.IRecipeProvider


class SlotType:
    INPUT = "enum:slottype:input"
    OUTPUT = "enum:slottype:output"
    PROVIDER = "enum:slottype:provider"


class ICraftingProvider:
    def __init__(self, inventory: gui.Inventory.Inventory, recipeprovider: crafting.IRecipeProvider.IRecipeProvider,
                 info=None):
        self.inventory = inventory
        self.recipeprovider = recipeprovider
        self.TABLE = {SlotType.INPUT: self.update_input, SlotType.OUTPUT: self.update_output,
                      SlotType.PROVIDER: self.update_provider}
        self.table = {}
        self.info = info

    def add_slot(self, position, idname, type=SlotType.INPUT):
        slot = gui.Slot.Slot(position=position, allow_player_interaction=type in [SlotType.INPUT, SlotType.OUTPUT])
        slot.id_name = idname
        self.inventory.slots.append(slot)
        if idname not in self.table: self.table[idname] = []
        self.table[idname].append(slot)
        return slot

    def update_input(self, slot):
        self.recipeprovider.on_input_update(self, self.table)

    def update_output(self, slot):
        self.recipeprovider.on_output_update(self, self.table)

    def update_provider(self, slot):
        pass

