import chat.command.export.CommandExportRegistry


TEXTS = ["/export [subcommand] [*]: a big command",
         "for more information see /help export"]


class SubCommandHelp(chat.command.export.CommandExportRegistry.ISubCommand):
    @staticmethod
    def get_prefix():
        return "help"

    @staticmethod
    def execute(line):
        print(*TEXTS, sep="\n")

    @staticmethod
    def get_help():
        return ["/export help: shows some informations about /export"]


chat.command.export.CommandExportRegistry.SUBCOMMANDS.append(SubCommandHelp)

