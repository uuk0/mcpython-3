import globals as G
import gui.Inventory
import pyglet
from pyglet.window import key
import chat.command.CommandHandler
import chat.command.CommandParser
import gui.TextDraw
import math

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
                       key.PLUS: "~", key.Q: "@@", key.LESS: "|"}}

for _key in KEYBOARD["lower"].keys():
    m = KEYBOARD["lower"][_key]
    u = m.upper()
    if m != u and _key not in KEYBOARD["upper"]:
        KEYBOARD["upper"][_key] = u


class Chat(gui.Inventory.Inventory):
    def __init__(self):
        self.text = ""
        self.history = []
        self.historyindex = -1
        self.init((0, 0))
        self.__blink_state = False
        self.__blink_timer = 0

    def draw(self):
        pyglet.gl.glColor3d(0, 0, 0)
        l = G.window.get_size()[0] - 5
        pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES,
                                     [0, 1, 2, 0, 2, 3],
                                     ('v2i', (5, 7,
                                              l, 7,
                                              l, 27,
                                              5, 27))
                                     )
        pyglet.gl.glColor3d(1, 1, 1)
        mlenght = math.ceil((G.window.get_size()[0] - 10) / 8) - 4
        text = self.text if not self.__blink_state else self.text[:-1]
        if len(text) > mlenght: text = text[len(text)-mlenght:]
        # print(text)
        gui.TextDraw.draw_string((text if not self.__blink_state else text + "_"), (10, 10))

    def on_event(self, name, *args, **kwargs):
        if name == "update":
            self.__blink_timer += args[0]
            if self.__blink_timer > 0.5:
                self.__blink_state = not self.__blink_state
                self.__blink_timer -= 0.5
                if self.__blink_state:
                    self.text += "_"
                else:
                    self.text = self.text[:-1]
        elif name == "on_key_press":
            ikey, modifiers = tuple(args)
            if ikey == 65288:  # BACK
                self.remove_characters(1)
            elif ikey == key.ENTER:  # execute command / send to system
                text = self.text
                G.inventoryhandler.hide_inventory(self)
                while len(text) > 0 and text[-1] == "_":
                    text = text[:-1]
                G.commandparser.parse_command(text)
                self.history.insert(0, text)
            elif modifiers & key.LSHIFT:
                if ikey in KEYBOARD["upper"]:
                    self.add_text(KEYBOARD["upper"][ikey])
            elif modifiers & key.RALT:
                if ikey in KEYBOARD["alt gr"]:
                    self.add_text(KEYBOARD["alt gr"][ikey])
            else:
                if ikey in KEYBOARD["lower"]:
                    self.add_text(KEYBOARD["lower"][ikey])
                elif ikey == key.UP and self.historyindex < len(self.history) - 1:
                    self.historyindex += 1
                    self.text = self.history[self.historyindex]
                elif ikey == key.DOWN and self.historyindex >= 0:
                    self.historyindex -= 1
                    if self.historyindex == -1:
                        self.text = ""
                    else:
                        self.text = self.history[self.historyindex]

    def add_text(self, text):
        if self.__blink_state:
            self.text = self.text[:-1] + text + "_"
        else:
            self.text += text

    def remove_characters(self, amount):
        if self.__blink_state:
            self.text = self.text[:-1-amount] + "_"
        else:
            self.text = self.text[:-amount]

    def on_close(self):
        self.text = ""
        self.historyindex = -1
        self.__blink_state = False
        self.__blink_timer = 0

    def on_open(self):
        self.text = ""
        self.historyindex = -1
        self.__blink_state = False
        self.__blink_timer = 0

    def print_msg(self, text):
        print("[CHAT] "+str(text))
