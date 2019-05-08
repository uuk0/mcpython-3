import globals as G
import importlib, os
import modloader.events.LoadStageEvent


class BlockHandler:
    def __init__(self):
        self.blocks = {}
        self.blockarray = []

    def __call__(self, *args, **kwargs):
        iblock = args[0]
        name = iblock.getName().split(":")
        for i in range(len(name)):
            self.blocks[":".join(name[i:])] = iblock
        self.blockarray.append(args[0])

    def register(self, klass):
        self(klass)


G.blockhandler = BlockHandler()


# @modloader.events.LoadStageEvent.blocks("minecraft")
# def load_blocks(*args):

for file in os.listdir(G.local+"/Block"):
    if file.startswith("Block") and file not in ["BlockHandler.py"]:
        @modloader.events.LoadStageEvent.blocks("minecraft", "loading "+str(file.split(".")[0]),
                                                arguments=[file])
        def load_file(eventname, filename):
            importlib.import_module("Block."+str(filename.split(".")[0]))

