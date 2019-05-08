"""
an system to sent new recipes to. contains code for dealing with recipes & gui's for the recipes.
only an abstract class system, with some useful code fragments
"""


class IRecipeProvider:
    def __init__(self):
        pass

    @staticmethod
    def get_recipe_type_name():
        raise NotImplementedError()

    def add_recipe(self, recipe):
        raise NotImplementedError()

    def get_recipe_class(self):
        return

    def on_input_update(self, icraftingprovider, table):
        pass

    def on_output_update(self, icraftingprovider, table):
        pass

