import globals as G
import rendering.blockrenderer.IBlockRenderer
import rendering.blockrenderer.Box
import Block.ILog


class IMultiRender(rendering.blockrenderer.IBlockRenderer.IBlockRenderer):
    @staticmethod
    def getName():
        return "imultirender"

    def __init__(self, *args, **kwargs):
        rendering.blockrenderer.IBlockRenderer.IBlockRenderer.__init__(self, *args, **kwargs)

    def show(self, iblock):
        for index in self.get_sub_indexes(iblock):
            iblockrenderer = self.model.entrys[index]
            iblockrenderer.show(iblock)

    def get_sub_indexes(self, iblock):
        """
        :return: an list of indexes in these model representing all parts of these model
        """
        raise NotImplementedError()

    def get_all_sub_indexes(self):
        raise NotImplementedError()

    def is_part_of(self, position):
        iblock = G.worldaccess.get_active_dimension_access().get_block(position, raise_exc=False)
        if not iblock: return
        for index in self.get_sub_indexes(iblock):
            iblockrenderer = self.model.entrys[index]
            if iblockrenderer.is_part_of(position):
                return True
        return False

    def get_texture_changes(self, start_index):
        data = []
        for index in self.get_all_sub_indexes():
            iblockrenderer = self.model.entrys[index]
            td = iblockrenderer.get_texture_changes(start_index)
            start_index += len(td)
            data += td
        return data


