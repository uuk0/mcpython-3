import Block.IRedstoneCircutePart
import globals as G


@G.blockhandler
class RedstoneBlock(Block.IRedstoneCircutePart.IRedstoneCircutePart):
    def on_create(self):
        self.inject_redstone_value(15)

    @staticmethod
    def getName():
        return "minecraft:redstone_block"

