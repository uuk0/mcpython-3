import globals as G
import pyglet
import util.progressbarrender


class ILoadingStage:
    def __init__(self, caption=""):
        self.active_stage = -1
        self.sub_stages = []
        self.sublevel = None
        self.progressbar = util.progressbarrender.ProgressBarRenderer((0, 0), 0, 400, 0, title=caption, height=15)

    def add_sub_stage(self, stage):
        self.sub_stages.append(stage)
        if self.sublevel:
            stage.sublevel = self.sublevel + 1

    def draw(self):
        sizex, sizez = G.window.get_size()
        psizex, psizez = self.progressbar.pixel_lenght, self.progressbar.height
        self.progressbar.position = (sizex//2-psizex//2, sizez//2-psizez//2+100-self.sublevel*20)
        self.progressbar.max_lenght = len(self.sub_stages)
        self.progressbar.draw()
        if 0 <= self.active_stage < len(self.sub_stages):
            self.sub_stages[self.active_stage].draw()

    def step(self) -> bool:
        """
        :return: weither the stage is completed or not
        """
        if self.active_stage == -1:
            self.on_stage_enter()
            self.active_stage += 1
            return False
        if not self.active_stage >= len(self.sub_stages) and self.sub_stages[self.active_stage].step():
            self.active_stage += 1
        if self.active_stage >= len(self.sub_stages):
            self.on_stage_leave()
            return True

    def on_stage_enter(self):
        pass

    def on_stage_leave(self):
        pass

