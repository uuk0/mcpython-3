import globals as G
import modloader.IMod


@G.modhandler
class ModHelperPluginAPI(modloader.IMod.IMod):
    @staticmethod
    def on_load():
        print(ModHelperPluginAPI.getDisplayName()+" is loading")

    @staticmethod
    def getName():
        return "modhelper:plugins"

    @classmethod
    def getDisplayName(cls):
        return "Mod Helper - Plugin API"

    @staticmethod
    def getLoadMode():
        return modloader.IMod.LoadMode.POST

    @staticmethod
    def getDependencies():
        return ["modhelper"]

