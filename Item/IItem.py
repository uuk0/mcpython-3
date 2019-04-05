import globals as G


class IItem:
    def __init__(self):
        pass

    @staticmethod
    def getName():
        raise NotImplementedError()

    def getItemFile(self):
        return G.local+"/tmp/missing_texture.png"
