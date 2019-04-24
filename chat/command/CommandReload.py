import globals as G
import chat.command.ICommand
import chat.command.CommandEntrys
import gui.ItemStack


@G.commandhandler
class Reload(chat.command.ICommand.ICommand):
    @staticmethod
    def get_prefix():
        return "reload"

    @staticmethod
    def get_syntax():
        return []

    @staticmethod
    def execute_command(line, parsed_values):
        chunks = list(G.worldaccess.get_active_dimension_access().chunks.values())
        chunks.sort(key=lambda chunkaccess: chunkaccess.position[0] + chunkaccess.position[1])
        for chunkaccess in chunks[:]:
            if not chunkaccess.visable or len(chunkaccess.world) == 0:
                chunks.remove(chunkaccess)
        for chunkaccess in chunks:
            if chunkaccess.visable:
                print("reloading chunk "+str(chunkaccess.position))
                G.window.set_caption('Mcpython build ' + str(G.CONFIG["BUILD"]) + " | /reload | "+str(
                    chunkaccess.position)+" | "+str(chunks.index(chunkaccess))+" / "+str(len(chunks)))
                index = 1
                m = len(chunkaccess.world)
                stepsize = round(m / 100) if m > 100 else 1
                for position in chunkaccess.world.keys():
                    chunkaccess.check_visable_state_of(position)
                    if index % stepsize == 0:
                        G.window.set_caption('Mcpython build ' + str(G.CONFIG["BUILD"]) + " | /reload | " + str(
                            chunkaccess.position) + " | " + str(chunks.index(chunkaccess)+1) + " / " + str(len(chunks)) +
                                             " | "+str(round(index/m*100))+"%")
                    index += 1
        G.window.set_caption('Mcpython build ' + str(G.CONFIG["BUILD"]))

    @staticmethod
    def get_help_lines():
        return ["/reload: reload all current visable blocks"]

