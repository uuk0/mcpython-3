"""
file for transforming textures for other things
"""

import PIL.Image, PIL.ImageDraw, PIL.ImageOps
import globals as G
import os


# Player Inventory

os.makedirs(G.local+"/tmp/gui/player")

image = PIL.Image.open(G.local+"/assets/textures/gui/container/inventory.png")
main = image.crop((0, 0, 176, 166))
main = main.resize((main.size[0] * 2, main.size[1] * 2))
main.save(G.local+"/tmp/gui/player/main.png")

image = PIL.Image.open(G.local+"/assets/textures/gui/widgets.png")
hotbar = image.crop((0, 0, 182, 22))
hotbar = hotbar.resize((182 * 2, 22 * 2))
hotbar.save(G.local+"/tmp/gui/player/hotbar.png")

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

mask = PIL.Image.open(G.local+"/assets/textures/block/oak_leaves.png").convert("L")

oak_leaves = PIL.Image.new("RGBA", (16, 16), (0, 0, 0, 0))

for x in range(16):
    for y in range(16):
        color = mask.getpixel((x, y))
        if color != 0:
            oak_leaves.putpixel((x, y), (color * 48 // 255, color * 116 // 255, color * 17 // 255, 255))


oak_leaves.save(G.local+"/tmp/blocks/leaves/oak_leave_default.png")

