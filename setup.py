import pyglet


def setup_fog():
    """ Configure the OpenGL fog properties.

    """
    # Enable fog. Fog "blends a fog color with each rasterized pixel fragment's
    # post-texturing color."
    pyglet.gl.glEnable(pyglet.gl.GL_FOG)
    # Set the fog color.
    pyglet.gl.glFogfv(pyglet.gl.GL_FOG_COLOR, (pyglet.gl.GLfloat * 4)(0.5, 0.69, 1.0, 1))
    # Say we have no preference between rendering speed and quality.
    pyglet.gl.glHint(pyglet.gl.GL_FOG_HINT, pyglet.gl.GL_DONT_CARE)
    # Specify the equation used to compute the blending factor.
    pyglet.gl.glFogi(pyglet.gl.GL_FOG_MODE, pyglet.gl.GL_LINEAR)
    # How close and far away fog starts and ends. The closer the start and end,
    # the denser the fog in the fog range.
    pyglet.gl.glFogf(pyglet.gl.GL_FOG_START, 20.0)
    pyglet.gl.glFogf(pyglet.gl.GL_FOG_END, 60.0)


def setup():
    """ Basic OpenGL configuration.

    """
    # Set the color of "clear", i.e. the sky, in rgba.
    pyglet.gl.glClearColor(0.5, 0.69, 1.0, 1)
    # Enable culling (not rendering) of back-facing facets -- facets that aren't
    # visible to you.
    pyglet.gl.glEnable(pyglet.gl.GL_CULL_FACE)
    # Set the texture minification/magnification function to GL_NEAREST (nearest
    # in Manhattan distance) to the specified texture coordinates. GL_NEAREST
    # "is generally faster than GL_LINEAR, but it can produce textured images
    # with sharper edges because the transition between texture elements is not
    # as smooth."
    pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MIN_FILTER, pyglet.gl.GL_NEAREST)
    pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MAG_FILTER, pyglet.gl.GL_NEAREST)
    setup_fog()

