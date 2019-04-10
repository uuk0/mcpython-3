import globals as G


class ICommandEntry:
    def is_valid(self, line, startindex):
        raise NotImplementedError()

    def get_value(self, line, startindex):
        raise NotImplementedError()

    def get_lenght(self, line, startindex):
        raise NotImplementedError()


class SelectorEntry(ICommandEntry):
    def __init__(self, valid_player=True, valid_pasive_entity=False, valid_aggressive_entity=False,
                 valid_item=False):
        self.valid_player = valid_player
        self.valid_pasive_entity = valid_pasive_entity
        self.valid_aggressive_entity = valid_aggressive_entity
        self.valid_item = valid_item

    def is_valid(self, line, startindex): return line[startindex].startswith("@")

    def get_value(self, line, startindex):
        item = line[startindex]
        if item == "@s" and self.valid_player:
            return [G.player] # experimental, may be ported to real entity
        return []

    def get_lenght(self, line, startindex):
        return 1


class ItemEntry(ICommandEntry):
    def __init__(self, block_valid=True, item_valid=True):
        self.block_valid = block_valid
        self.item_valid = item_valid

    def is_valid(self, line, startindex):
        return True

    def get_value(self, line, startindex):
        itemname = line[startindex]
        if itemname in G.itemhandler.classes:
            return itemname
        elif itemname in G.itemhandler.itemnametofile:
            return itemname
        return None

    def get_lenght(self, line, startindex):
        return 1


class IntEntry(ICommandEntry):
    def is_valid(self, line, startindex):
        try:
            int(line[startindex])
        except:
            return False
        return True

    def get_value(self, line, startindex):
        try:
            return int(line[startindex])
        except:
            return None

    def get_lenght(self, line, startindex):
        return 1

