import globals as G
import gui.ItemStack
import pyglet
import Item.ItemHandler

IMAGE_SIZE = (100, 100)


class Slot:
    def __init__(self, stack_or_item_or_name=None, amount=None, position=(0, 0),
                 is_valid_item_function=None, allow_player_interaction=True, update_func=None):
        if type(stack_or_item_or_name) != gui.ItemStack.ItemStack:
            stack_or_item_or_name = gui.ItemStack.ItemStack(stack_or_item_or_name, amount if amount else 1)
        stack_or_item_or_name.amount = amount if amount else stack_or_item_or_name.amount
        self.__stack = stack_or_item_or_name
        self.label = pyglet.text.Label(text=str(self.stack.amount), color=(0, 0, 0, 255))
        self.label.x, self.label.y = position[0] + IMAGE_SIZE[0], position[1] + IMAGE_SIZE[1]
        self.sprite = pyglet.sprite.Sprite(pyglet.image.load(G.local+"/tmp/missing_texture.png"))
        self.sprite.position = position
        self.position = position
        self.__itemfile = G.local+"/tmp/missing_texture.png"
        self.__depend = []
        self.is_valid_item_function = is_valid_item_function
        self.allow_player_interaction = allow_player_interaction
        self.update_func = update_func

    def is_player_interaction_allowed(self):
        return self.allow_player_interaction

    def get_stack(self):
        return self.__stack

    def __set_stack(self, stack):
        self.set_stack(stack)

    def set_stack(self, stack: gui.ItemStack.ItemStack):
        if self.is_valid_item_function and not self.is_valid_item_function(stack):
            return False
        self.__stack = stack
        if self.update_func: self.update_func(self)
        return True

    stack = property(get_stack, __set_stack)

    def add_depend(self, slot):
        self.__depend.append(slot)

    def move_relative(self, rpos):
        x, y = self.position
        x += rpos[0]
        y += rpos[1]
        self.position = (x, y)
        self.label.x, self.label.y = x + IMAGE_SIZE[0], y + IMAGE_SIZE[1]

    def draw(self):
        if self.stack and self.stack.item.getItemFile() if self.stack.item else self.stack.itemfile:
            if self.stack.amount <= 0:
                self.stack = gui.ItemStack.ItemStack.empty()
                return
            if self.position != self.sprite.position:
                self.sprite.position = self.position
                self.label.x = self.position[0] + 30
                self.label.y = self.position[1] - 2

            file = self.stack.item.getItemFile() if self.stack.item else self.stack.itemfile
            if file != self.__itemfile:
                self.__itemfile = file
                self.sprite.image = pyglet.image.load(file)
            self.sprite.draw()
            if self.stack.amount != 1:
                self.label.text = str(self.stack.amount)
                self.label.draw()

    def move_to(self, position):
        self.position = position
        self.sprite.position = position
        self.label.x = position[0] + 20
        self.label.y = position[1] + 20

    def set_item(self, item, amount=1):
        self.stack.set_item(item)
        self.stack.set_amount(amount)
        if self.update_func: self.update_func(self)

    def get_item(self):
        return self.stack.item


class SlotCopy(Slot):
    def __init__(self, copyof: Slot, position=(0, 0)):
        copyof.add_depend(self)
        self.position = position
        self.master = copyof
        self.sprite = pyglet.sprite.Sprite(pyglet.image.load(G.local+"/tmp/missing_texture.png"))
        self.__itemfile = G.local + "/tmp/missing_texture.png"
        self.label = pyglet.text.Label(text=str(self.master.stack.amount), color=(0, 0, 0, 255))
        self.label.x, self.label.y = position[0] + IMAGE_SIZE[0], position[1] + IMAGE_SIZE[1]

    def add_depend(self, slot):
        self.master.add_depend(slot)

    def move_relative(self, rpos):
        x, y = self.position
        x += rpos[0]
        y += rpos[1]
        self.position = (x, y)
        self.label.x, self.label.y = x + IMAGE_SIZE[0], y + IMAGE_SIZE[1]

    def draw(self):
        if self.master.stack and self.master.stack.itemfile:
            if self.get_stack().amount <= 0:
                self.set_stack(gui.ItemStack.ItemStack.empty())
            if self.position != self.sprite.position:
                self.sprite.position = self.position
                self.label.x = self.position[0] + 30
                self.label.y = self.position[1] - 2

            file = self.master.stack.item.getItemFile() if self.master.stack.item else self.master.stack.itemfile
            if file != self.__itemfile:
                self.__itemfile = file
                self.sprite.image = pyglet.image.load(file)
            self.sprite.draw()
            if self.master.stack.amount != 1:
                self.label.text = str(self.master.stack.amount)
                self.label.draw()

    def move_to(self, position):
        self.position = position
        self.sprite.position = position
        self.label.x = position[0] + 20
        self.label.y = position[1] + 20

    def set_item(self, item, amount=1):
        self.master.set_item(item, amount)

    def get_item(self):
        return self.master.stack.item

    def get_stack(self):
        return self.master.stack

    def __set_stack(self, stack):
        self.set_stack(stack)

    def set_stack(self, stack: gui.ItemStack.ItemStack):
        return self.master.set_stack(stack)

    stack = property(get_stack, __set_stack)

    def is_player_interaction_allowed(self):
        return self.master.allow_player_interaction

