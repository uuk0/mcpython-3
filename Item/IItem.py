import globals as G


class IItem:
    def __init__(self):
        self.enchantments = []

    @staticmethod
    def getName():
        raise NotImplementedError()

    def getItemFile(self):
        return G.local+"/tmp/missing_texture.png"

    def getBlockName(self):
        return self.getName()

    def getMaxStackSize(self):
        return 64

    @staticmethod
    def has_block():
        return True

    def enchant(self, enchantment):
        self.enchantments.append(enchantment)

    def is_enchantable_with(self, enchantment):
        return True
