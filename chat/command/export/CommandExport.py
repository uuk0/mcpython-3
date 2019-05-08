"""
Is this weired? a whole directory for a single command? but these command contains a lot of code
for exporting informations out of the game into other structures
"""

import globals as G
import chat.command.ICommand
import chat.command.CommandEntrys
import gui.ItemStack
import chat.command.export.CommandExportRegistry
from . import (SubCommandHelp, SubCommandBiomeMap)


@G.commandhandler
class CommandExport(chat.command.ICommand.ICommand):
    @staticmethod
    def get_prefix():
        return "export"

    @staticmethod
    def get_syntax():
        return []

    @staticmethod
    def execute_command(line, parsed_values):
        if len(line) == 1: line.append("help")
        for isubcommand in chat.command.export.CommandExportRegistry.SUBCOMMANDS:
            if isubcommand.get_prefix() == line[1]:
                isubcommand.execute(line)
                return
        print("error: /export can't cast command '"+str(line[1])+"'")

    @staticmethod
    def get_help_lines():
        pages = []
        for isubcommand in chat.command.export.CommandExportRegistry.SUBCOMMANDS:
            pages += isubcommand.get_help()
        return pages

