import globals as G
import importlib, os


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

    def create_block_at(self, position, name):
        return None if name not in self.blocks else self.blocks[name](position)


G.blockhandler = BlockHandler()


for file in os.listdir(G.local+"/Block"):
    if file.startswith("Block") and not file in ["BlockHandler.py"]:
        importlib.import_module("Block."+str(file.split(".")[0]))

