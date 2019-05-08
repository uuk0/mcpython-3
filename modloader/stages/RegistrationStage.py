import modloader.stages.ILoadingStage
import modloader.stages.StageLoadHandler
import globals as G
import time


class RegistrationStage(modloader.stages.ILoadingStage.ILoadingStage):
    def on_stage_enter(self):
        pass

    def on_stage_leave(self):
        pass


mainstage = RegistrationStage(caption="registrating things")
G.stageloadhandler.add_stage(mainstage)

