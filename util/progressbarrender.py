"""
main renderer for progressbars in these project
designed only for these project, licenced under MIT-licence - so you can use it anywhere you want
"""

import pyglet
# from pyglet.gl import *
import gui.TextDraw
from PIL import Image


class ProgressBarRenderer:
    def __init__(self, position, max_lenght, pixel_lenght, progress, title="", height=10,
                 outer_line_color=(0, 0, 0), progress_color=(0, 0, 0), text_color=(0, 0, 0)):
        """
        create an progressbar
        :param position: where to render it
        :param max_lenght: how big gets progress?
        :param pixel_lenght: how weight should it be
        :param progress: the progress to display
        :param title: the title to show above
        :param height: the height of the progress bar
        :param outer_line_color: which color the outer line should have
        :param progress_color: which color the progress should have
        :param text_color: the color in which the text should be rendered
        """
        self.position = position
        self.max_lenght = max_lenght
        self.pixel_lenght = pixel_lenght
        self.progress = progress
        self.title = title
        self.height = height
        self.outer_line_color = outer_line_color
        self.progress_color = progress_color
        self.text_color = text_color
        self.label = pyglet.text.Label(text=self.title)

    def draw(self):
        if self.max_lenght == 0: return
        x, y = self.position
        dx = self.pixel_lenght
        dy = self.height
        pyglet.gl.glColor3d(*self.outer_line_color)
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (x, y, x, y + dy)))
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (x, y, x + dx, y)))
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (x+dx, y, x+dx, y + dy)))
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (x, y+dy, x+dx, y + dy)))
        pyglet.gl.glColor3d(*self.progress_color)
        dx = round((self.progress / self.max_lenght) * self.pixel_lenght)
        pyglet.gl.glColor3d(*self.progress_color)
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (x, y,
                                                             x + dx, y,
                                                             x + dx, y + dy,
                                                             x, y + dy)))
        if self.title != "":
            # self.label.color = self.text_color
            self.label.text = str(self.title)
            self.label.x = x + dx // 2 - len(self.title) * 8 // 2
            self.label.y = y + dy + 5
            self.label.draw()
            # gui.TextDraw.draw_string(self.title, (x + dx // 2 - len(self.title) * 8, y + dy + 5))
        pyglet.gl.glColor3d(1, 1, 1)

