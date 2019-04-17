
import Block.ILog
import globals as G


@G.blockhandler
class OakLog(Block.ILog.ILog):
    @staticmethod
    def getName():
        return "minecraft:oak_log"

