
import Block.ILog
import globals as G


@G.blockhandler
class BoneBlock(Block.ILog.ILog):
    @staticmethod
    def getName():
        return "minecraft:bone_block"

