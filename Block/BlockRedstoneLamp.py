import Block.IRedstoneCircutePart
import globals as G


@G.blockhandler
class RedstoneLamp(Block.IRedstoneCircutePart.IRedstoneCircutePart):
    @staticmethod
    def getName():
        return "minecraft:redstone_lamp"

    def get_active_model_index(self):
        v = self.get_surrounding_redstone_values()
        if len(v) == 0: return 0
        return 0 if self.injected_redstone_value <= 0 and max(self.get_surrounding_redstone_values()) == 0 else 1

    def on_redstone_update(self):
        if self.is_visable:
            G.modelhandler.hide(self)
            G.modelhandler.show(self)

