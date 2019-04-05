import globals as G
import json


class IStructure:
    def __init__(self, *args, **kwargs):
        pass

    def paste(self, x, y, z):
        pass

    @staticmethod
    def getStructureType():
        return "surface"  # possible: surface


class StructureFile(IStructure):
    def __init__(self, file):
        self.file = file
        with open(file) as f:
            self.data = json.load(f)

    def paste(self, x, y, z):
        for rx, ry, rz in self.data["blocks"].keys():
            nx, ny, nz = x + rx, y + ry, z + rz
            blockname = self.data["blocktable"][self.data["blocks"]]
            G.model.add_block((nx, ny, nz), blockname)

