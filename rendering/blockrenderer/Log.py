import globals as G
import rendering.blockrenderer.IBlockRenderer
import rendering.blockrenderer.IMultiRender
import rendering.blockrenderer.Box
import Block.ILog


class LogModelEntry(rendering.blockrenderer.IMultiRender.IMultiRender):
    @staticmethod
    def getName():
        return "log"

    def __init__(self, *args, **kwargs):
        rendering.blockrenderer.IMultiRender.IMultiRender.__init__(self, *args, **kwargs)
        self.indexes = [self.data["front_index"], self.data["side_index"]]
        self.sindexes = []

    def on_create(self):
        # generate entrys an add them to model
        self.sindexes += list(range(len(self.model.entrys), len(self.model.entrys)+3))
        self.model.entrys.append(rendering.blockrenderer.Box.BoxModelEntry(
            {"name": "cube", "indexes": [self.indexes[0]]*2+[self.indexes[1]]*4}, self.model))
        self.model.entrys.append(rendering.blockrenderer.Box.BoxModelEntry(
            {"name": "cube", "indexes": [self.indexes[1], self.indexes[2]] +
                                        [self.indexes[0]] * 2 + [self.indexes[2]] * 2}, self.model))
        self.model.entrys.append(rendering.blockrenderer.Box.BoxModelEntry(
            {"name": "cube", "indexes": [self.indexes[2], self.indexes[1]] +
                                        [self.indexes[2]] * 2 + [self.indexes[0]] * 2}, self.model))

    def get_texture_changes(self, start_index):
        default = rendering.blockrenderer.IMultiRender.IMultiRender.get_texture_changes(self, start_index)
        start_index += len(default)
        self.indexes.append(start_index)
        return [{"type": "rotate",
                 "files": [self.indexes[1]],
                 "arguments": [90]}] + default

    def get_sub_indexes(self, iblock):
        """
        :return: an list of indexes in these model representing all parts of these model
        """
        if issubclass(type(iblock), Block.ILog.ILog):
            orientation = iblock.get_rotation()
            if orientation == "OW":
                return [self.sindexes[2]]
            elif orientation == "NS":
                return [self.sindexes[1]]
            else:  # default is UD
                return [self.sindexes[0]]

    def get_all_sub_indexes(self):
        return self.sindexes


rendering.blockrenderer.IBlockRenderer.ENTRYS[LogModelEntry.getName()] = LogModelEntry

