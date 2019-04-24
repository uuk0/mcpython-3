import globals as G
import chat.command.ICommand
import chat.command.CommandEntrys
import util.vector
import modloader.events.LoadStageEvent


ITEMS_PER_PAGE = 10


@G.commandhandler
class Help(chat.command.ICommand.ICommand):
    PAGES = []

    @staticmethod
    def get_prefix():
        return "help"

    @staticmethod
    def get_syntax():
        return []

    @staticmethod
    def execute_command(line, parsed_values):
        if len(line) > 1:
            element = line[1]
            try:
                element = int(element)
            except:
                if element.startswith("/"): element = element[1:]
                if element not in G.commandhandler.commands:
                    print("error: command not found: "+str(element))
                    return
                print("help to command " + str(element))
                icommand = G.commandhandler.commands[element]
                print(*icommand.get_help_lines(), sep="\n")
                return
        else:
            element = 1
        print(*Help.PAGES[element-1], sep="\n")

    @staticmethod
    def get_help_lines():
        return ["/help [{page_or_command=1: int/str<with or without '/'>}]: returns help"]


def load_startup():
    commands = G.commandhandler.commands.values()
    pages = []
    for icommand in commands:
        pages += icommand.get_help_lines()
    pages.sort()
    for i in range(len(pages)//ITEMS_PER_PAGE+1):
        i *= ITEMS_PER_PAGE
        if i + ITEMS_PER_PAGE - 1 >= len(pages):
            Help.PAGES.append(pages[i:])
        else:
            Help.PAGES.append(pages[i:i+ITEMS_PER_PAGE])

