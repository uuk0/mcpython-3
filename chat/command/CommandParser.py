import globals as G


class CommandParser:
    def __init__(self):
        pass

    def parse_command(self, line: str):
        if not line.startswith("/"):
            G.player.chat.print_msg(line)
            return
        splitted = line.split(" ")
        prefix = splitted[0][1:]
        if prefix not in G.commandhandler.commands:
            G.player.chat.print_msg("[ERROR] command not found")
            return
        icommand = G.commandhandler.commands[prefix]
        index = 1
        values = []
        for icommandentry in icommand.get_syntax():
            if icommandentry.is_valid(splitted, index):
                values.append(icommandentry.get_value(splitted, index))
                index += icommandentry.get_lenght(splitted, index)
            else:
                G.player.chat.print_msg("[ERROR] element "+str(index)+" is not valid command entry for "+
                                        str(icommandentry))
        return icommand.execute_command(splitted, values)


G.commandparser = CommandParser()

