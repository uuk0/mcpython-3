import globals as G
import gui.Inventory
import pyglet
from pyglet.window import key
import chat.command.CommandHandler
import chat.command.CommandParser

KEYBOARD = {"lower": {key.A: "a", key.B: "b", key.C: "c", key.D: "d", key.E: "e", key.F: "f", key.G: "g",
                      key.H: "h", key.I: "i", key.J: "j", key.K: "k", key.L: "l", key.M: "m", key.N: "n",
                      key.O: "o", key.P: "p", key.Q: "q", key.R: "r", key.S: "s", key.T: "t", key.U: "u",
                      key.V: "v", key.W: "w", key.X: "x", key.Y: "y", key.Z: "z", key.SPACE: " ",
                      key._0: "0", key._1: "1", key._2: "2", key._3: "3", key._4: "4", key._5: "5", key._6: "6",
                      key._7: "7", key._8: "8", key._9: "9", key.HASH: "#", key.PLUS: "+", key.MINUS: "-",
                      44: ",", 46: ".", key.LESS: "<", key.NUM_0: "0", key.NUM_1: "1",
                      key.NUM_2: "2", key.NUM_3: "3", key.NUM_4: "4", key.NUM_5: "5", key.NUM_6: "6",
                      key.NUM_7: "7", key.NUM_8: "8", key.NUM_9: "9"},
            "upper": {key._1: "!", key._2: '"', key._3: "§", key._4: "$", key._5: "%", key._6: "&",
                      key._7: "/", key._8: "(", key._9: ")", key._0: "=", key.PLUS: "*", key.HASH: "'",
                      46: ":", 44: ";", key.MINUS: "_", key.LESS: ">"},
            "alt gr": {key._2: "²", key._3: "³", key._7: "{", key._8: "[", key._9: "]", key._0: "}",
                       key.PLUS: "~", key.Q: "@", key.LESS: "|"}}


class Chat(gui.Inventory.Inventory):
    def __init__(self):
        self.label = pyglet.text.Label(color=(0, 0, 0, 255), bold=True)
        self.init((0, 0))
        self.__blink_state = False
        self.__blink_timer = 0

    def draw(self):
        self.label.x, self.label.y = (10, 10)
        self.label.draw()

    def on_event(self, name, *args, **kwargs):
        if name == "update":
            self.__blink_timer += args[0]
            if self.__blink_timer > 0.5:
                self.__blink_state = not self.__blink_state
                self.__blink_timer -= 0.5
                if self.__blink_state:
                    self.label.text += "_"
                else:
                    self.label.text = self.label.text[:-1]
        elif name == "on_key_press":
            ikey, modifiers = tuple(args)
            if ikey == 65288:  # BACK
                self.remove_characters(1)
            elif ikey == key.ENTER:  # execute command / send to system
                text = self.label.text
                G.inventoryhandler.hide_inventory(self)
                while text[-1] == "_":
                    text = text[:-1]
                G.commandparser.parse_command(text)
            elif modifiers & key.LSHIFT:
                if ikey in KEYBOARD["upper"]:
                    self.add_text(KEYBOARD["upper"][ikey])
            elif modifiers & key.RALT:
                if ikey in KEYBOARD["alt gr"]:
                    self.add_text(KEYBOARD["alt gr"][ikey])
            else:
                if ikey in KEYBOARD["lower"]:
                    self.add_text(KEYBOARD["lower"][ikey])

    def add_text(self, text):
        if self.__blink_state:
            self.label.text = self.label.text[:-1] + text + "_"
        else:
            self.label.text += text

    def remove_characters(self, amount):
        if self.__blink_state:
            self.label.text = self.label.text[:-1-amount] + "_"
        else:
            self.label.text = self.label.text[:-amount]

    def on_close(self):
        self.label.text = ""
        self.__blink_state = False
        self.__blink_timer = 0

    def on_open(self):
        self.label.text = ""
        self.__blink_state = False
        self.__blink_timer = 0

    def print_msg(self, text):
        print("[CHAT] "+str(text))
