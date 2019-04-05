"""
function around vertices
"""


def cube_vertices(x, y, z, nx, ny=None, nz=None):
    """ Return the vertices of the cube at position x, y, z with size 2*n.

    """
    if ny == None: ny = nx
    if nz == None: nz = nx
    return [
        x - nx, y + ny, z - nz, x - nx, y + ny, z + nz, x + nx, y + ny, z + nz, x + nx, y + ny, z - nz,  # top
        x - nx, y - ny, z - nz, x + nx, y - ny, z - nz, x + nx, y - ny, z + nz, x - nx, y - ny, z + nz,  # bottom
        x - nx, y - ny, z - nz, x - nx, y - ny, z + nz, x - nx, y + ny, z + nz, x - nx, y + ny, z - nz,  # left
        x + nx, y - ny, z + nz, x + nx, y - ny, z - nz, x + nx, y + ny, z - nz, x + nx, y + ny, z + nz,  # right
        x - nx, y - ny, z + nz, x + nx, y - ny, z + nz, x + nx, y + ny, z + nz, x - nx, y + ny, z + nz,  # front
        x + nx, y - ny, z - nz, x - nx, y - ny, z - nz, x - nx, y + ny, z - nz, x + nx, y + ny, z - nz,  # back
    ]


def tex_coord(x, y, n=16):
    """ Return the bounding vertices of the texture square.

    """
    m = 1.0 / n
    dx = x * m
    dy = y * m
    return dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m


def tex_coords(top, bottom, n, e, s, w):
    """ Return a list of the texture squares for the top, bottom and sides.

    """
    top = tex_coord(*top)
    bottom = tex_coord(*bottom)
    n = tex_coord(*n)
    e = tex_coord(*e)
    s = tex_coord(*s)
    w = tex_coord(*w)
    result = []
    result.extend(top)
    result.extend(bottom)
    result.extend(n)
    result.extend(e)
    result.extend(s)
    result.extend(w)
    return result

