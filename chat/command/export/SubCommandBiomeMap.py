import chat.command.export.CommandExportRegistry
import globals as G
import PIL.Image
import util.vector


TEXTS = ["/export biomemap store [area x start] [area z start] [area x end] [area z end] " +
         "[file or none to store to default]: save the current biome map in area to the given file or default"]


BIOMECOLORS = {"minecraft:dessert": (204, 204, 0, 255),
               "minecraft:dessert_hills": (255, 255, 51, 255),
               "minecraft:gravelly_mountains": (137, 137, 118, 255),
               "minecraft:mountains": (164, 164, 150, 255),
               "minecraft:ocean": (0, 255, 0, 255),
               "minecraft:wooded_mountains": (105, 105, 91, 255),
               "minecraft:plains": (0, 255, 0, 255),
               "minecraft:sunflower_plains": (0, 59, 0, 255)}


class SubCommandBiomeMap(chat.command.export.CommandExportRegistry.ISubCommand):
    @staticmethod
    def get_prefix():
        return "biomemap"

    @staticmethod
    def execute(line):
        if len(line) == 2:
            print("/export biomemap error: can't find an castable command")
            return
        command = line[2]
        if command == "store":
            fromx, fromz, tox, toz = tuple([int(x) for x in line[3:7]])
            file = G.local+"/tmp/biomemap.png" if len(line) == 7 else line[7]
            image = PIL.Image.new("RGBA", ((tox-fromx+1)*16, (toz-fromz)*16))
            for cx in range(fromx, tox+1):
                for cz in range(fromz, toz+1):
                    print((cx, cz))
                    G.worldaccess.get_active_dimension_access().\
                        worldgenerationprovider.biomemap.generate_for_chunk((cx, cz))
            for x in range(fromx*16, tox*16+16):
                for y in range(fromz*16, toz*16):
                    if (x, y) not in G.worldaccess.get_active_dimension_access().worldgenerationprovider.biomemap.map:
                        G.worldaccess.get_active_dimension_access().worldgenerationprovider.biomemap.generate_for_chunk(
                            util.vector.sectorize((x, 0, y))
                        )
                    biome = G.worldaccess.get_active_dimension_access(). \
                            worldgenerationprovider.biomemap[(x, y)]
                    color = (0, 0, 0, 255) if biome.getName() not in BIOMECOLORS else \
                        BIOMECOLORS[biome.getName()]
                    rx, ry = x, y
                    rx -= fromx * 16
                    ry -= fromz * 16
                    # print((rx, ry))
                    try:
                        image.putpixel((rx, ry), color)
                    except:
                        pass
            image.save(file)
            G.worldaccess.get_active_dimension_access().worldgenerationprovider.biomemap.bordermap.\
                generate_border_image_an_save_at(G.local+"/tmp/border.png")
        else:
            print("/export biomemap error: can't cast "+str(command)+" to an valid command")

    @staticmethod
    def get_help():
        return ["/export help: shows some informations about /export"]


chat.command.export.CommandExportRegistry.SUBCOMMANDS.append(SubCommandBiomeMap)

