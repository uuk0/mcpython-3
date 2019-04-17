import Block.IBlock


class ILog(Block.IBlock.IBlock):
    def __init__(self, *args, **kwargs):
        Block.IBlock.IBlock.__init__(self, *args, **kwargs)
        self.rotation = None
        self.update_rotation()

    def update_rotation(self):
        if self.previous:
            dx = abs(self.position[0] - self.previous[0])
            dy = abs(self.position[1] - self.previous[1])
            dz = abs(self.position[2] - self.previous[2])
            if dx:
                self.rotation = "NS"
            elif dy:
                self.rotation = "UD"
            elif dz:
                self.rotation = "OW"
            else:
                self.rotation = None

    def get_rotation(self):
        return "UD" if not self.rotation else self.rotation

