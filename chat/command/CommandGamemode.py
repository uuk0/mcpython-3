import globals as G
import chat.command.ICommand
import chat.command.CommandEntrys
import gui.ItemStack


@G.commandhandler
class Gammeode(chat.command.ICommand.ICommand):
    @staticmethod
    def get_prefix():
        return "gamemode"

    @staticmethod
    def get_syntax():
        return [chat.command.CommandEntrys.IntEntry()]

    @staticmethod
    def execute_command(line, parsed_values):
        G.player.set_gamemode(parsed_values[0])

    @staticmethod
    def get_help_lines():
        return ["/gamemode <id>: set the gamemode of the player"]

