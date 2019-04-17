import Block.IBlock
import globals as G


class ISlab(Block.IBlock.IBlock):
    def __init__(self, *args, mode=None, **kwargs):
        Block.IBlock.IBlock.__init__(self, *args, **kwargs)
        self.mode = mode
        if self.hitposition and not mode:
            dy = self.position[1] - self.hitposition[1]
            if dy < 0:
                self.mode = "up"
            else:
                self.mode = "down"

    def get_state(self):
        # possible: "up", "down", "double"
        return "down" if not self.mode else self.mode

    def is_solid_to(self, position):
        dy = self.position[1] - position[1]
        return (dy < 0 and self.mode == "up") or (dy > 0 and self.mode == "down")

    def can_interact_with(self, itemstack, mousekey=None, mousemod=None):
        return False
        #todo: reimplement these system
        return itemstack.itemname == self.getName()

    def on_interact_with(self, itemstack, mousekey=None, mousemod=None):
        return
        itemstack.amount -= 1
        G.model.add_block(self.position, self.getName(), mode="double")
        return itemstack, False

    def get_drop(self, itemstack):
        return {self.getName(): 2 if self.mode == "double" else 1}

