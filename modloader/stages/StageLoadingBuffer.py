import modloader.stages.ILoadingStage


class StageLoadingBuffer(modloader.stages.ILoadingStage.ILoadingStage):
    def __init__(self, stagename, *args, functions_loading=[], functions_loading_end=[], **kwargs):
        modloader.stages.ILoadingStage.ILoadingStage.__init__(self, *args, **kwargs)
        self.stagename = stagename
        self.function_loading = functions_loading
        self.functions_loading_end = functions_loading_end
        if self.progressbar.title == "":
            self.progressbar.title = "loading phase "+str(self.stagename)

    def on_stage_enter(self):
        print("loading stage "+str(self.stagename))
        for function in self.function_loading:
            function(self.stagename, "enter")

    def on_stage_leave(self):
        for function in self.functions_loading_end:
            function(self.stagename, "leave")


class StageLoadingBufferNotation(modloader.stages.ILoadingStage.ILoadingStage):
    def __init__(self, eventname, modname, function, *args, action=None, arguments=[], **kwargs):
        modloader.stages.ILoadingStage.ILoadingStage.__init__(self, *args, **kwargs)
        self.modname = modname
        self.action = action
        if self.progressbar.title == "":
            self.progressbar.title = "mod "+str(modname)+" is loading "+str(self.action if action else "")
        self._function = function
        self.eventname = eventname
        self.arguments = arguments

    def function(self, *args, **kwargs):
        self._function(*list(args)+list(self.arguments), **kwargs)

    def on_stage_enter(self):
        if self.action:
            print(" -mod "+str(self.modname)+" is registrating "+str(self.action))
        self.function(self.eventname)

    def on_stage_leave(self):
        pass

