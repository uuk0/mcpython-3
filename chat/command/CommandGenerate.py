import globals as G
import chat.command.ICommand
import chat.command.CommandEntrys
import util.vector


@G.commandhandler
class Generate(chat.command.ICommand.ICommand):
    @staticmethod
    def get_prefix():
        return "generate"

    @staticmethod
    def get_syntax():
        return []

    @staticmethod
    def execute_command(line, parsed_values):
        chunk = util.vector.sectorize(G.window.position)
        G.worldaccess.get_active_dimension_access().worldgenerationprovider.generate_chunk(chunk)

    @staticmethod
    def get_help_lines():
        return ["/generate: generates the chunk you are in"]

