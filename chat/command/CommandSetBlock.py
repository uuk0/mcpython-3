import globals as G
import chat.command.ICommand
import chat.command.CommandEntrys
import gui.ItemStack
import random


@G.commandhandler
class Setblock(chat.command.ICommand.ICommand):
    @staticmethod
    def get_prefix():
        return "setblock"

    @staticmethod
    def get_syntax():
        return [chat.command.CommandEntrys.PositionEntry(),
                chat.command.CommandEntrys.BlockEntry(enable_multible_blocks=True)]

    @staticmethod
    def execute_command(line, parsed_values):
        position = parsed_values[0]
        blockarray = parsed_values[1]
        G.worldaccess.get_active_dimension_access().add_block(position, random.choice(blockarray))

    @staticmethod
    def get_help_lines():
        return ["/setblock [x] [y] [z] [blockname]: set the block at the given position"]

