import pyglet
import PIL.Image
import globals as G


class ICharacterAccess:
    def get_image_at(self, index):
        raise NotImplementedError()

    def get_image_from_char(self, char):
        raise NotImplementedError()


def get_hex_view_of_I(I, min_size=2):
    v = hex(I)[2:]
    while len(v) < min_size: v = "0" + v
    return v


class UnicodePage(ICharacterAccess):
    def __init__(self, file, unicode_size=(16, 16), index=None):
        if not index:
            # format: unicode_page_[...].png
            index = int(file.split("/")[-1].split("\\")[-1].split(".")[0].split("_")[-1])
        self.index = index
        self.imagesequenz = pyglet.image.ImageGrid(pyglet.image.load(file), *unicode_size)
        self.table = {}
        self.spritetable = {}
        self.size = unicode_size
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                self.table["@U"+get_hex_view_of_I(index)+get_hex_view_of_I(x)+get_hex_view_of_I(y)+"@"] = (x, y)

    def get_image_at(self, index):
        x, y = index
        x = self.size[0] - x - 1
        return self.imagesequenz[(x, y)]

    def get_image_from_char(self, char):
        return self.get_image_at(self.table[char])

    def draw_at(self, char, position):
        index = self.table[char]
        if index not in self.spritetable:
            self.spritetable[index] = pyglet.sprite.Sprite(self.get_image_at(index))
        self.spritetable[index].position = position
        self.spritetable[index].draw()


page_00 = UnicodePage(G.local+"/assets/textures/font/unicode_page_00.png")
page_00.table = {" ": (2, 0), "!": (2, 1), '"': (2, 2), "#": (2, 3), "$": (2, 4), "%": (2, 5), "&": (2, 6), "'": (2, 7),
                 "(": (2, 8), ")": (2, 9), "*": (2, 10), "+": (2, 11), ",": (2, 12), "-": (2, 13), ".": (2, 14),
                 "/": (2, 15), "0": (3, 0), "1": (3, 1), "2": (3, 2), "3": (3, 3), "4": (3, 4), "5": (3, 5),
                 "6": (3, 6), "7": (3, 7), "8": (3, 8), "9": (3, 9), ":": (3, 10), ";": (3, 11), "<": (3, 12),
                 "=": (3, 13), ">": (3, 14), "?": (3, 15), "@": (4, 0), "A": (4, 1), "B": (4, 2), "C": (4, 3),
                 "D": (4, 4), "E": (4, 5), "F": (4, 6), "G": (4, 7), "H": (4, 8), "I": (4, 9), "J": (4, 10),
                 "K": (4, 11), "L": (4, 12), "M": (4, 13), "N": (4, 14), "O": (4, 15), "P": (5, 0), "Q": (5, 1),
                 "R": (5, 2), "S": (5, 3), "T": (5, 4), "U": (5, 5), "V": (5, 6), "W": (5, 7), "X": (5, 8),
                 "Y": (5, 9), "Z": (5, 10), "[": (5, 11), "\\": (5, 12), "]": (5, 13), "^": (5, 14), "_": (5, 15),
                 "`": (6, 0), "a": (6, 1), "b": (6, 2), "c": (6, 3), "d": (6, 4), "e": (6, 5), "f": (6, 6),
                 "g": (6, 7), "h": (6, 8), "i": (6, 9), "j": (6, 10), "k": (6, 11), "l": (6, 12), "m": (6, 13),
                 "n": (6, 14), "o": (6, 15), "p": (7, 0), "q": (7, 1), "r": (7, 2), "s": (7, 3), "t": (7, 4),
                 "u": (7, 5), "v": (7, 6), "w": (7, 7), "x": (7, 8), "y": (7, 9), "z": (7, 10), "{": (7, 11),
                 "|": (7, 12), "}": (7, 13), "~": (7, 14), "§": (10, 7)}


PAGES = [page_00]


def draw_string(chars: str, position, line_height=16, char_weight=8):
    x, y, = position
    charlist = []
    index = 0
    while index < len(chars):
        c = chars[index]
        index += 1
        if c == "@":  # select symbols that are extra (in @...@)
            if index < len(chars) and chars[index] == "@":
                charlist.append("@")
                index += 1
            else:
                charlist.append(chars[index-1: chars.index("@", index)+1])
                index = chars.index("@", index) + 1
        else:
            charlist.append(c)
    for char in charlist:
        if char == "\n":
            y -= line_height
            x = position[0]
        elif char == " ":
            x += char_weight
        else:
            flag = True
            for page in PAGES:
                if char in page.table and flag:
                    page.draw_at(char, (x, y))
                    x += char_weight
                    flag = False
            if flag:
                print("can't access char '"+str(char)+"'")

