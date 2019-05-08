
import Block.ILog
import globals as G


@G.blockhandler
class SpruceLog(Block.ILog.ILog):
    @staticmethod
    def getName():
        return "minecraft:spruce_log"

