"""
file for transforming textures for other things
"""

import PIL.Image, PIL.ImageDraw, PIL.ImageOps
import globals as G
import os
import modloader.events.LoadStageEvent


class Info:
    hotbar_size = None
    main_size = None


def overlayhelper(mask, coloring):
    mask = mask.convert("L")

    image = PIL.Image.new("RGBA", mask.size, (0, 0, 0, 0))

    for x in range(16):
        for y in range(16):
            color = mask.getpixel((x, y))
            if color != 0:
                image.putpixel((x, y), (color * coloring[0] // 255, color * coloring[1] // 255,
                                              color * coloring[2] // 255, 255))

    return image


@modloader.events.LoadStageEvent.texture_setup("minecraft")
def setup_textures(*args):

    # Player Inventory

    os.makedirs(G.local+"/tmp/gui/player")

    image = PIL.Image.open(G.local+"/assets/textures/gui/container/inventory.png")
    main = image.crop((0, 0, 176, 166))
    main = main.resize((main.size[0] * 2, main.size[1] * 2))
    main.save(G.local+"/tmp/gui/player/main.png")

    Info.main_size = main.size

    image = PIL.Image.open(G.local+"/assets/textures/gui/widgets.png")
    hotbar = image.crop((0, 0, 182, 22))
    hotbar = hotbar.resize((182 * 2, 22 * 2))
    hotbar.save(G.local+"/tmp/gui/player/hotbar.png")

    Info.hotbar_size = hotbar.size

    hotbar_select = image.crop((0, 23, 23, 45))
    hotbar_select = hotbar_select.resize((hotbar_select.size[0]*2, hotbar_select.size[0]*2))
    hotbar_select.save(G.local+"/tmp/gui/player/hotbar_select.png")

    # Missing Texture

    missing_texture = PIL.Image.new("RGBA", (16, 16), color=(255, 0, 255))

    draw = PIL.ImageDraw.Draw(missing_texture)

    draw.rectangle([0, 0, 7, 7], fill=(0, 0, 0, 255))
    draw.rectangle([8, 8, 16, 16], fill=(0, 0, 0, 255))

    del draw

    missing_texture.save(G.local+"/tmp/missing_texture.png")

    # Leaves

    os.makedirs(G.local+"/tmp/blocks/leaves")

    overlayhelper(PIL.Image.open(G.local+"/assets/textures/block/oak_leaves.png"),
                  (48, 116, 17)).save(G.local+"/tmp/blocks/leaves/oak_leave_default.png")

    overlayhelper(PIL.Image.open(G.local + "/assets/textures/block/spruce_leaves.png"),
                  (48, 116, 17)).save(G.local + "/tmp/blocks/leaves/spruce_leave_default.png")

    # Grass (the block from which seeds drop)

    overlayhelper(PIL.Image.open(G.local + "/assets/textures/block/grass.png"),
                  (50, 128, 17)).save(G.local + "/tmp/blocks/grass_small.png")

    overlayhelper(PIL.Image.open(G.local + "/assets/textures/block/tall_grass_top.png"),
                  (50, 128, 17)).save(G.local + "/tmp/blocks/tall_grass_top.png")

    overlayhelper(PIL.Image.open(G.local + "/assets/textures/block/tall_grass_bottom.png"),
                  (50, 128, 17)).save(G.local + "/tmp/blocks/tall_grass_bottom.png")

