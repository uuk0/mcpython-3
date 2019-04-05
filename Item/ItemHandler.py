import globals as G


class ItemHandler:
    def __init__(self):
        self.itemnametofile = {}
        self.classes = {}

    def register(self, obj):
        if type(obj) == list:
            name = obj[0]
            for i in range(len(name)):
                self.itemnametofile[":".join(name[i:])] = obj[1]
        else:
            name = obj.getName()
            for i in range(len(name)):
                self.itemnametofile[":".join(name[i:])] = obj.getItemFile(None)
                self.classes[":".join(name[i:])] = obj

    def __call__(self, *args, **kwargs):
        self.register(args[0])


G.itemhandler = ItemHandler()

