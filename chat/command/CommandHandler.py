import globals as G
import modloader.events.LoadStageEvent


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


@modloader.events.LoadStageEvent.commands("minecraft")
def load_commands(eventname):
    from . import (CommandGive, CommandClear, CommandGamemode, CommandReload, CommandGenerate, CommandHelp)


@modloader.events.LoadStageEvent.load_finished("minecraft")
def load_startup(eventname):
    import chat.command.CommandHelp
    chat.command.CommandHelp.load_startup()

