import globals as G
import chat.command.ICommand
import chat.command.CommandEntrys
import gui.ItemStack


@G.commandhandler
class Clear(chat.command.ICommand.ICommand):
    @staticmethod
    def get_prefix():
        return "clear"

    @staticmethod
    def get_syntax():
        return []

    @staticmethod
    def execute_command(line, parsed_values):
        slots = G.player.playerinventory.POSSIBLE_MODES["hotbar"].slots + \
                G.player.playerinventory.POSSIBLE_MODES["inventory"].slots[9:]
        for slot in slots:
            slot.set_stack(gui.ItemStack.ItemStack.empty())

    @staticmethod
    def get_help_lines():
        return ["/clear: clear the inventory"]

