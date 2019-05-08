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
        if not (iblock.shown_data and "vertex_data" in iblock.shown_data): return
        for vertexdata in iblock.shown_data["vertex_data"]:
            try:
                vertexdata.delete()
            except:
                pass

    def is_part_of(self, position):
        return True

    def get_texture_changes(self, start_index):
        return []

    def store_vertex_data(self, iblock, vertexdata: list):
        if not iblock.shown_data: iblock.shown_data = {}
        if "vertex_data" not in iblock.shown_data:
            iblock.shown_data["vertex_data"] = []
        iblock.shown_data["vertex_data"] += vertexdata

    def on_create(self):
        pass

