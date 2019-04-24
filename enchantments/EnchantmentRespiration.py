import enchantments.IEnchantment
import Item.ItemEnchantedBook


class Respiration(enchantments.IEnchantment.IEnchantment):
    def enable(self):
        pass

    def disable(self):
        pass

    @classmethod
    def is_valid_body(cls, body):
        try:
            if issubclass(type(body), Item.ItemEnchantedBook.EnchantedBook):  # enchanted book is OK
                return True
        except:
            return False

    @classmethod
    def get_possible_levels(cls):
        return [1, 2, 3]

    @staticmethod
    def getName():
        return "respiration"

