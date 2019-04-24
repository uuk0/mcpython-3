import globals as G
import modloader.IMod


@G.modhandler
class ModHelper(modloader.IMod.IMod):
    @staticmethod
    def on_load():
        print(ModHelper.getDisplayName()+" is loading")

    @staticmethod
    def getName():
        return "modhelper"

    @classmethod
    def getDisplayName(cls):
        return "Mod Helper"

