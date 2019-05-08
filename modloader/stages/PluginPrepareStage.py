import modloader.stages.ILoadingStage
import modloader.stages.StageLoadHandler
import globals as G
import time


class PluginPrepareStage(modloader.stages.ILoadingStage.ILoadingStage):
    def on_stage_enter(self):
        pass

    def on_stage_leave(self):
        pass


mainstage = PluginPrepareStage(caption="registrating plugins")
G.stageloadhandler.add_stage(mainstage)

