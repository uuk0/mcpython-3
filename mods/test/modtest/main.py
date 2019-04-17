import globals as G
import modloader.IMod
import modloader.events.LoadStageEvent


print("I'm a test: 'Hello World!'")


@G.modhandler
class ModTest(modloader.IMod.IMod):
    @staticmethod
    def getName():
        return "modtest"

    @staticmethod
    def getVersionID():
        return 0


@modloader.events.LoadStageEvent.startup("modtest")
def on_startup(*args):
    print("hello from startup phase")

