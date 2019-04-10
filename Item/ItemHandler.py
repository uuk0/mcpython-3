import globals as G
import PIL.Image
import importlib, os


class ItemHandler:
    def __init__(self):
        self.itemnametofile = {}
        self.classes = {}
        self.itemnames = []

    def register(self, obj):
        if type(obj) == list:
            name = obj[0].split(":")
            for i in range(len(name)):
                self.itemnametofile[":".join(name[i:])] = obj[1]
            self.itemnames.append(obj[0])
        else:
            name = obj.getName().split(":")
            for i in range(len(name)):
                self.itemnametofile[":".join(name[i:])] = obj.getItemFile(None)
                self.classes[":".join(name[i:])] = obj
            self.itemnames.append(obj.getName())
            file = obj.getItemFile(None)
            image = PIL.Image.open(file)
            image.resize((32, 32)).save(file)

    def __call__(self, *args, **kwargs):
        self.register(args[0])


G.itemhandler = ItemHandler()


for file in os.listdir(G.local+"/Item"):
    if file.startswith("Item") and not file in ["ItemHandler.py"]:
        importlib.import_module("Item."+str(file.split(".")[0]))

