import globals as G
import chat.command.ICommand
import chat.command.CommandEntrys


@G.commandhandler
class Give(chat.command.ICommand.ICommand):
    @staticmethod
    def get_prefix():
        return "give"

    @staticmethod
    def get_syntax():
        return [chat.command.CommandEntrys.SelectorEntry(valid_pasive_entity=False, valid_aggressive_entity=False,
                                                         valid_item=False),
                chat.command.CommandEntrys.ItemEntry()]

    @staticmethod
    def execute_command(line, parsed_values):
        # print(line, parsed_values)
        for player in parsed_values[0]:
            player.add_to_free_place(parsed_values[1], 1 if len(line) == 3 else int(line[3]))

    @staticmethod
    def get_help_lines():
        return ["/give {selector} {itemname: string[nbt]} [{amount=1: int}]: give the selected entitys (players) " +
                "the given item by amount"]

