import globals as G
import gui.ItemStack
import pyglet
import Item.ItemHandler

missing_texture = pyglet.image.load(G.local+"/tmp/blocks/leaves/oak_leave_default.png")

IMAGE_SIZE = (100, 100)


class Slot:
    def __init__(self, stack_or_item_or_name=None, amount=None, position=(0, 0)):
        if type(stack_or_item_or_name) != gui.ItemStack.ItemStack:
            stack_or_item_or_name = gui.ItemStack.ItemStack(stack_or_item_or_name, amount if amount else 1)
        stack_or_item_or_name.amount = amount if amount else stack_or_item_or_name.amount
        self.stack = stack_or_item_or_name
        self.label = pyglet.text.Label(text=str(self.stack.amount))
        self.label.x, self.label.y = position[0] + IMAGE_SIZE[0], position[1] + IMAGE_SIZE[1]
        self.sprite = pyglet.sprite.Sprite(missing_texture)
        self.sprite.position = position
        self.position = position
        self.__itemfile = G.local+"/tmp/missing_texture.png"

    def move_relative(self, rpos):
        x, y = self.position
        x += rpos[0]
        y += rpos[1]
        self.position = (x, y)
        self.label.x, self.label.y = x + IMAGE_SIZE[0], y + IMAGE_SIZE[1]

    def draw(self):
        if self.stack and self.stack.itemfile:
            if self.position != self.sprite.position:
                self.sprite.position = self.position

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

