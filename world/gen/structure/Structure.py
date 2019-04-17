import globals as G
import json


class IStructure:
    def paste(self, x, y, z):
        pass

    @staticmethod
    def getStructureType():
        return "surface"  # possible: surface, height

    def getStructureGenerationChance(self) -> int:
        return 0

    def is_valid(self, x, y, z, height) -> bool:
        return True


class IHeightStructure(IStructure):
    @staticmethod
    def getStructureType():
        return "height"

    def get_min(self) -> int:
        raise NotImplementedError()

    def get_max(self) -> int:
        raise NotImplementedError()


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

