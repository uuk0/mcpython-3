import globals as G
import crafting.RecipeType


class CraftingHandler:
    def __init__(self):
        self.recipes = {}
        self.recipetypes = {}

    def register_recipe_type(self, recipetype: crafting.RecipeType.RecipeType):
        self.recipes[recipetype.name] = {}
        self.recipetypes[recipetype.name] = recipetype

    def add_recipe(self, recipetypename, gridname, recipe):
        if recipetypename not in self.recipetypes:
            raise ValueError()
        if self.recipetypes[recipetypename].valid_function and \
                not self.recipetypes[recipetypename].valid_function(gridname, recipe):
            raise ValueError()
        if not gridname in self.recipes[recipetypename]: self.recipes[recipetypename] = []
        self.recipes[recipetypename][gridname].append(recipe)


G.craftinghandler = CraftingHandler()

