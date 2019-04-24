import globals as G
import rendering.blockrenderer.IBlockRenderer
import rendering.blockrenderer.Box
import Block.ILog


class LogModelEntry(rendering.blockrenderer.IBlockRenderer.IBlockRenderer):
    @staticmethod
    def getName():
        return "log"

    def __init__(self, *args, **kwargs):
        rendering.blockrenderer.IBlockRenderer.IBlockRenderer.__init__(self, *args, **kwargs)
        self.sub_model = rendering.blockrenderer.Box.BoxModelEntry({}, self.model)
        self.indexes = [self.data["front_index"], self.data["side_index"]]

    def show(self, position):
        self.update_submodel_for(position)
        self.sub_model.show(position)

    def hide(self, position):
        self.update_submodel_for(position)
        self.sub_model.hide(position)

    def update_submodel_for(self, block):
        # block = G.model.world[position]
        if issubclass(type(block), Block.ILog.ILog):
            orientation = block.get_rotation()
            if orientation == "UD":
                self.sub_model.data = {"name": "cube", "indexes": [self.indexes[0]]*2+[self.indexes[1]]*4}
            elif orientation == "NS":
                self.sub_model.data = {"name": "cube", "indexes": [self.indexes[1], self.indexes[2]] +
                                                                  [self.indexes[0]]*2 + [self.indexes[2]]*2}
            elif orientation == "OW":
                self.sub_model.data = {"name": "cube", "indexes": [self.indexes[2], self.indexes[1]] +
                                                                  [self.indexes[2]]*2 + [self.indexes[0]]*2}
            else:
                raise ValueError("rotation "+str(orientation)+" is unknown")
        else:
            raise ValueError("position contains block that is not supported")

    def is_part_of(self, position):
        # self.update_submodel_for(position)
        return self.sub_model.is_part_of(position)

    def get_texture_changes(self, start_index):
        self.indexes.append(start_index)
        return [{"type": "rotate",
                 "files": [self.indexes[1]],
                 "arguments": [90]}]


rendering.blockrenderer.IBlockRenderer.ENTRYS[LogModelEntry.getName()] = LogModelEntry