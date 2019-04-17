import globals as G


class ILoadStageEvent:
    def __init__(self, name):
        self.name = name
        self.tasks = {}
        self.__buffer = ILoadStageEventBuffer(self)
        self.__buffer_modname = None
        self.depend = []
        self.op_depend = []
        self.depends = []
        self.__closed = False

    def __call__(self, modname):
        if self.__closed:
            raise RuntimeError("try to notate to an closed stage")
        self.__buffer_modname = modname
        if modname not in self.tasks:
            self.tasks[modname] = []
        return self.__buffer

    def register_func(self, func):
        self.tasks[self.__buffer_modname].append(func)
        return func

    def close(self):
        self.__closed = True


class ILoadStageEventBuffer:
    def __init__(self, event: ILoadStageEvent):
        self.event = event

    def __call__(self, func):
        self.event.register_func(func)
        return func

