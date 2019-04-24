ENTRYS = {}


class IBlockRenderer:
    def __init__(self, entrydata, model):
        self.data = entrydata
        self.model = model

    @staticmethod
    def getName():
        return ""

    def show(self, iblock):
        pass

    def hide(self, iblock):
        pass

    def is_part_of(self, position):
        return True

    def get_texture_changes(self, start_index):
        return []


