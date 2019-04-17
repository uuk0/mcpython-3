
import Block.ILog
import globals as G


@G.blockhandler
class QuartzPillar(Block.ILog.ILog):
    @staticmethod
    def getName():
        return "minecraft:quartz_pillar"

