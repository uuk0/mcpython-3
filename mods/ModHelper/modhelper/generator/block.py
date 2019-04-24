import globals as G
import Block.IBlock
import Block.ILog
import Block.ISlab


def construct_cube(modelfile, blockname=None,
                   brakeable=True, modelindex=0, drop=None, solid=True):
    if modelfile not in G.modelhandler.models:
        G.modelhandler.add_model(modelfile)
    model = G.modelhandler.models[modelfile]
    if not blockname: blockname = model.name

    @G.blockhandler
    class ConstructedBlock(Block.IBlock.IBlock):
        @staticmethod
        def getName():
            return blockname

        def get_active_model_index(self):
            return modelindex

        def get_model_name(self):
            return model.name

        def get_drop(self, itemstack):
            return {self.getName(): 1} if not drop else drop

        def isBrakeAble(self):
            return brakeable

        def is_solid(self):
            return solid

    return ConstructedBlock



