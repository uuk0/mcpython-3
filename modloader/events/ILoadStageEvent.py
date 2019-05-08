import globals as G
import modloader.stages.StageLoadingBuffer


class ILoadStageEvent:
    def __init__(self, name, superloadingstage=None):
        self.name = name
        self.tasks = {}
        self.__buffer = ILoadStageEventBuffer(self)
        self.__buffer_modname = None
        self.__buffer_action = None
        self.__buffer__arguments = None
        self.depend = []
        self.op_depend = []
        self.depends = []
        self.__closed = False
        self.superloadingstage = superloadingstage
        self.stage = modloader.stages.StageLoadingBuffer.StageLoadingBuffer(name)
        if superloadingstage:
            superloadingstage.add_sub_stage(self.stage)

    def __call__(self, modname, action=None, arguments=[]):
        if self.__closed:
            raise RuntimeError("try to notate to an closed stage")
        self.__buffer_modname = modname
        self.__buffer_action = action
        self.__buffer__arguments = arguments
        if modname not in self.tasks:
            self.tasks[modname] = []
        return self.__buffer

    def register_func(self, func):
        self.tasks[self.__buffer_modname].append(func)
        self.stage.add_sub_stage(
            modloader.stages.StageLoadingBuffer.StageLoadingBufferNotation(self.name, self.__buffer_modname, func,
                                                                           action=self.__buffer_action,
                                                                           arguments=self.__buffer__arguments))
        return func

    def close(self):
        self.__closed = True


class ILoadStageEventBuffer:
    def __init__(self, event: ILoadStageEvent):
        self.event = event

    def __call__(self, func):
        self.event.register_func(func)
        return func

