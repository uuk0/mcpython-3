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

    def is_valid(self, line, startindex): return line[startindex].startswith("@@")

    def get_value(self, line, startindex):
        item = line[startindex]
        if item == "@@s" and self.valid_player:
            return [G.player]  # experimental, may be ported to real entity
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


class PositionEntry(ICommandEntry):
    def is_valid(self, line, startindex):
        item_1 = line[startindex]
        # area for making it possible to use @... as positions
        # if SelectorEntry.is_valid(None, [item_1], 0):
        #     return True
        if len(line) >= startindex + 3:
            item_2 = line[startindex+1]
            item_3 = line[startindex+2]
            if IntEntry.is_valid(None, [item_1], 0) and IntEntry.is_valid(None, [item_2], 0) and \
                    IntEntry.is_valid(None, [item_3], 0):
                return True
        return False

    def get_value(self, line, startindex):
        item_1 = line[startindex]
        item_2 = line[startindex + 1]
        item_3 = line[startindex + 2]
        return IntEntry.get_value(None, [item_1], 0), IntEntry.get_value(None, [item_2], 0), \
                 IntEntry.get_value(None, [item_3], 0)

    def get_lenght(self, line, startindex):
        return 3


class BlockEntry(ICommandEntry):
    def __init__(self, enable_multible_blocks=False):
        self.enable_multible_blocks = enable_multible_blocks

    def is_valid(self, line, startindex):
        blockinfo = line[startindex]
        blocknameinfos = blockinfo.split("|")
        for blocknameinfo in blocknameinfos:
            blockname = blocknameinfo.split(":")[0]
            if blockname not in G.blockhandler.blocks:
                return False
        return True

    def get_lenght(self, line, startindex):
        return 1

    def get_value(self, line, startindex):
        blockinfo = line[startindex]
        blocknameinfos = blockinfo.split("|")
        blocktable = []
        for blocknameinfo in blocknameinfos:
            info = blocknameinfo.split(":")
            blockname = info[0]
            blocktable += [G.blockhandler.blocks[blockname].getName()] * (1 if len(info) == 1 and
                                                                          self.enable_multible_blocks else
                                                                          int(info[1]))
        return blocktable


