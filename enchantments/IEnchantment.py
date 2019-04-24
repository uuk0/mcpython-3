import globals as G


class IEnchantment:
    def __init__(self, body, level=1):
        self.body = body
        self.level = level

    @staticmethod
    def getName(): raise NotImplementedError()

    def enable(self):
        pass

    def disable(self):
        pass

    @classmethod
    def is_valid_body(cls, body):
        return True

    @classmethod
    def get_possible_levels(cls):
        return [1]

