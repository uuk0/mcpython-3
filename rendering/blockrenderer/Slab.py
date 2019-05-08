import rendering.blockrenderer.IBlockRenderer
import rendering.blockrenderer.Box
import Block.ISlab


class SlabModelEntry(rendering.blockrenderer.IBlockRenderer.IBlockRenderer):
    @staticmethod
    def getName():
        return "slab"

    def __init__(self, *args, **kwargs):
        rendering.blockrenderer.IBlockRenderer.IBlockRenderer.__init__(self, *args, **kwargs)
        self.sub_model = rendering.blockrenderer.Box.BoxModelEntry({}, self.model)
        self.indexes = [self.data["side"], self.data["top"]]

    def show(self, position):
        self.update_submodel_for(position)
        self.sub_model.show(position)

    def hide(self, position):
        self.update_submodel_for(position)
        self.sub_model.hide(position)

    def update_submodel_for(self, block):
        # block = G.model.world[position]
        if issubclass(type(block), Block.ISlab.ISlab):
            mode = block.get_state()
            if mode == "up":
                self.sub_model.data = {"name": "cube",
                                       "indexes": [self.indexes[1]]*2+[self.indexes[2]]*4,
                                       "box_size": [0.5, 0.25, 0.5],
                                       "relative_position": [0, 0.25, 0]}
            elif mode == "down":
                self.sub_model.data = {"name": "cube",
                                       "indexes": [self.indexes[1]]*2+[self.indexes[3]]*4,
                                       "box_size": [0.5, 0.25, 0.5],
                                       "relative_position": [0, -0.25, 0]}
            elif mode == "double":
                self.sub_model.data = {"name": "cube", "indexes": [self.indexes[1]]*2+[self.indexes[0]]*4}
            else:
                raise ValueError("unknown state of slab: "+str(mode))
        else:
            raise ValueError("position cotains block that is not supported")

    def is_part_of(self, position):
        # self.update_submodel_for(position)
        return self.sub_model.is_part_of(position)

    def get_texture_changes(self, start_index):
        self.indexes += [start_index+1, start_index+3]
        return [{"type": "crop", "files": self.indexes[0], "arguments": [[[0, 7, 15, 15]]]},
                {"type": "resize", "files": start_index, "arguments": [[64, 64]]},
                {"type": "crop", "files": self.indexes[0], "arguments": [[[0, 0, 15, 7]]]},
                {"type": "resize", "files": start_index+2, "arguments": [[64, 64]]}]


rendering.blockrenderer.IBlockRenderer.ENTRYS[SlabModelEntry.getName()] = SlabModelEntry


