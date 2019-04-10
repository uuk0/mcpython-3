import globals as G
import crafting.Recipe


class RecipeType:
    def __init__(self, name):
        self.name = name
        self.valid_function = None
        self.preconsuming = False
        self.outputinputautoremoving = False

    def set_validate_function(self, *args):
        self.valid_function = args[0]

    def set_preconsuming(self, flag):
        self.preconsuming = flag

    def outputinputautoremoving(self, flag):
        self.outputinputautoremoving = flag


crafting_type = RecipeType("crafting")


@crafting_type.set_validate_function
def valid(grid, recipe):
    return type(recipe) == crafting.Recipe.Crafting


# G.craftinghandler.register_recipe_type(crafting_type)

