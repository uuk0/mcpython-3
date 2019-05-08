import modloader.stages.ILoadingStage
import modloader.stages.StageLoadHandler
import globals as G
import time


class FinishingUpHandler(modloader.stages.ILoadingStage.ILoadingStage):
    def on_stage_enter(self):
        pass

    def on_stage_leave(self):
        pass


mainstage = FinishingUpHandler(caption="finishing up...")
G.stageloadhandler.add_stage(mainstage)

