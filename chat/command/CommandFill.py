import globals as G
import chat.command.ICommand
import chat.command.CommandEntrys
import gui.ItemStack
import random


@G.commandhandler
class Setblock(chat.command.ICommand.ICommand):
    @staticmethod
    def get_prefix():
        return "fill"

    @staticmethod
    def get_syntax():
        return [chat.command.CommandEntrys.PositionEntry(),
                chat.command.CommandEntrys.PositionEntry(),
                chat.command.CommandEntrys.BlockEntry(enable_multible_blocks=True)]

    @staticmethod
    def execute_command(line, parsed_values):
        sx, sy, sz = parsed_values[0]
        ex, ey, ez = parsed_values[1]
        if sx > ex: ex, sx = sx, ex
        if sy > ey: ey, sy = sy, ey
        if sz > ez: ez, sz = sz, ez
        blockarray = parsed_values[2]
        dimensionaccess = G.worldaccess.get_active_dimension_access()
        for x in range(sx, ex+1):
            for y in range(sy, ey+1):
                for z in range(sz, ez+1):
                    dimensionaccess.add_block((x, y, z), random.choice(blockarray))

    @staticmethod
    def get_help_lines():
        return ["/fill [start x] [start y] [start z] [end x] [end y] [end z] [blockname]: fill the given area " +
                "with the given block"]

