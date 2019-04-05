import globals as G


class Inventory:
    def init(self, position):
        self.position = position
        import gui.InventoryHandler
        G.inventoryhandler.add_inventory(self)
        self.slots = self.create_slots()
        for slot in self.slots:
            slot.move_relative(self.position)

    def create_slots(self):
        return []

    def draw_background(self):
        pass

    def draw_overlay(self):
        pass

    def draw(self):
        self.draw_background()
        for slot in self.slots:
            slot.draw()
        self.draw_overlay()

    def is_blocking_interaction(self):
        return True

    def on_event(self, name, *args, **kwargs):
        pass

    def should_be_closed_by_esc(self):
        return True

    def is_only_esc_closed(self):
        return True

    def on_close(self):
        pass

    def on_open(self):
        pass

    def should_activate_mouse(self):
        return self.should_be_closed_by_esc()

