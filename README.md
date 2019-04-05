# mcpython-3
Mcpython is an minecraft clone written in pure python using pyglet as an OpenGL-binding

# Credits
the project is based on code from fogleman (can be found on https://github.com/fogleman/Minecraft)
it uses code segments from serval tutorials and wiki pages

# Project code
The Project is published at the moment in its raw form. No compilation, no obfuscation.
Please install Python 3.7.3 (tested), the libarys pyglet, pillow and simplexnoise and the code from this repo in order to play.

# How to play
When you start the game, you will see at the beginning an screen swithing between all blocks in the game.
Do not wonder, we are generting some pictures on startup. If you have some better code to do that (transform the blocks into reprsenting item files), please write to me.

The world generation is printed out into the consol. Per default, 3x3 chunks will be generated.

You can select blocks via 1-9 (not all accessable) or by simply clicking on the block with mouse middle

# Add new content

You can easely add new blocks by simply adding an model.json and load it and create an class extending Block.IBlock
