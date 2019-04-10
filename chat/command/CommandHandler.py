import globals as G


class CommandHandler:
    def __init__(self):
        self.commands = {}  # prefix -> command

    def register(self, icommand):
        prefix = icommand.get_prefix()
        self.commands[prefix] = icommand

    def __call__(self, *args, **kwargs):
        self.register(args[0])
        return args[0]


G.commandhandler = CommandHandler()


from . import (CommandGive, CommandClear, CommandGamemode)

