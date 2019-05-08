"""
main class for redstone circute part
"""

import globals as G
import Block.IBlock


class IRedstoneCircutePart(Block.IBlock.IBlock):
    def on_block_update(self, reason=None):
        self.on_redstone_update()

    def has_binding_to(self, position):
        return False

    def get_provided_power_to(self, position):
        return self.injected_redstone_value

    def on_redstone_update(self):
        pass

    def send_redstone_update(self):
        pass

    def get_redstone_level_to(self, position):
        return 0

    def get_surrounding_redstone_values(self):
        x, y, z = self.position
        sur = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                for dz in range(-1, 2):
                    if [dx, dy, dz].count(0) == 2:
                        nx, ny, nz = x + dx, y + dy, z + dz
                        iblock = G.worldaccess.get_active_dimension_access().get_block((nx, ny, nz), raise_exc=False)
                        if iblock:
                            sur.append(iblock.injected_redstone_value if not issubclass(type(iblock),
                                                                                        IRedstoneCircutePart) else
                                       iblock.get_provided_power_to(self.position))
        return sur


