import globals as G
import modloader.events.LoadStageEvent
import os
import importlib


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


for file in os.listdir(G.local+"/chat/command"):
    if file.startswith("Command") and file not in ["CommandHandler.py",
                                                   "CommandParser.py"]:
        @modloader.events.LoadStageEvent.commands("minecraft", "loading "+str(file.split(".")[0]),
                                                arguments=[file])
        def load_file(eventname, filename):
            importlib.import_module("chat.command."+str(filename.split(".")[0]))


@modloader.events.LoadStageEvent.commands("minecraft", "loading CommandExport")
def load_file(eventname):
    importlib.import_module("chat.command.export.CommandExport")


@modloader.events.LoadStageEvent.load_finished("minecraft")
def load_startup(eventname):
    import chat.command.CommandHelp
    chat.command.CommandHelp.load_startup()

