import globals as G


class IItem:
    def __init__(self):
        pass

    @staticmethod
    def getName():
        raise NotImplementedError()

    def getItemFile(self):
        return G.local+"/tmp/missing_texture.png"

    def getBlockName(self):
        return self.getName()

    def getMaxStackSize(self):
        return 64

    @staticmethod
    def has_block():
        return True
