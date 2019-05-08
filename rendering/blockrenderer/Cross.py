import globals as G
import rendering.blockrenderer.IBlockRenderer
import util.vertices
import util.vector
import pyglet


def cross_texture_1(x, y, z, nx, ny=None, nz=None):
    """ Return the vertices of the cube at position x, y, z with size 2*n.

    """
    if ny == None: ny = nx
    if nz == None: nz = nx
    return [
        x - nx, y + ny, z - nz, x - nx, y + ny, z - nz, x - nx, y + ny, z - nz, x - nx, y + ny, z - nz,  # top
        x - nx, y - ny, z - nz, x - nx, y - ny, z - nz, x - nx, y - ny, z - nz, x - nx, y - ny, z - nz,  # bottom
        x - nx, y - ny, z - nz, x - nx, y - ny, z - nz, x - nx, y - ny, z - nz, x - nx, y - ny, z - nz,  # left
        x + nx, y - ny, z + nz, x + nx, y - ny, z + nz, x + nx, y - ny, z + nz, x + nx, y - ny, z + nz,  # right
        x + nx, y - ny, z + nz, x - nx, y - ny, z - nz, x - nx, y + ny, z - nz, x + nx, y + ny, z + nz,  # back
        x - nx, y - ny, z - nz, x + nx, y - ny, z + nz, x + nx, y + ny, z + nz, x - nx, y + ny, z - nz  # front
    ]


def cross_texture_2(x, y, z, nx, ny=None, nz=None):
    """ Return the vertices of the cube at position x, y, z with size 2*n.

    """
    if ny == None: ny = nx
    if nz == None: nz = nx
    return [
        x - nx, y + ny, z - nz, x - nx, y + ny, z - nz, x - nx, y + ny, z - nz, x - nx, y + ny, z - nz,  # top
        x - nx, y - ny, z - nz, x - nx, y - ny, z - nz, x - nx, y - ny, z - nz, x - nx, y - ny, z - nz,  # bottom
        x - nx, y - ny, z - nz, x - nx, y - ny, z - nz, x - nx, y - ny, z - nz, x - nx, y - ny, z - nz,  # left
        x + nx, y - ny, z + nz, x + nx, y - ny, z + nz, x + nx, y - ny, z + nz, x + nx, y - ny, z + nz,  # right
        x - nx, y - ny, z + nz, x + nx, y - ny, z - nz, x + nx, y + ny, z - nz, x - nx, y + ny, z + nz,  # back
        x + nx, y - ny, z - nz, x - nx, y - ny, z + nz, x - nx, y + ny, z + nz, x + nx, y + ny, z - nz   # front
    ]


class CrossTextureModelEntry(rendering.blockrenderer.IBlockRenderer.IBlockRenderer):
    def __init__(self, *args, **kwargs):
        rendering.blockrenderer.IBlockRenderer.IBlockRenderer.__init__(self, *args, **kwargs)
        self.indexes = [self.data["face"]]

    @staticmethod
    def getName():
        return "cross"

    def show(self, iblock):
        if iblock.shown_data: self.hide(iblock)
        position = iblock.position
        textureatlas = G.textureatlashandler.atlases[self.model.indexes[0][0]]
        x, y, z = position
        rpos = (0, 0, 0)
        x += rpos[0]
        y += rpos[1]
        z += rpos[2]
        # vertex_data = util.vertices.cube_vertices(x, y, z, *area)
        indexes_1 = [self.indexes[0]] * 6
        data_1 = []
        for element in indexes_1:
            data_1.append(textureatlas.filearray[self.model.indexes[element][1]])
        texture_data_1 = list(util.vertices.tex_coords(*data_1))

        indexes_2 = [self.indexes[0]] * 6
        data_2 = []
        for element in indexes_2:
            data_2.append(textureatlas.filearray[self.model.indexes[element][1]])
        texture_data_2 = list(util.vertices.tex_coords(*data_2))
        # create vertex list
        # FIXME Maybe `add_indexed()` should be used instead
        chunk = util.vector.sectorize(position)
        chunkaccess = G.worldaccess.get_active_dimension_access().get_chunk_for(chunk)
        batch = chunkaccess.alpha_batch if "enable_alpha" not in self.data or self.data["enable_alpha"] else \
            chunkaccess.batch  # here we are using reverse alpha / non alpha config
        self.store_vertex_data(iblock, [batch.add(24, pyglet.gl.GL_QUADS, textureatlas.pygletatlas,
                                                  ('v3f/static', cross_texture_1(x, y, z, 0.5)),
                                                  ('t2f/static', texture_data_1)),
                                        batch.add(24, pyglet.gl.GL_QUADS, textureatlas.pygletatlas,
                                                  ('v3f/static', cross_texture_2(x, y, z, 0.5)),
                                                  ('t2f/static', texture_data_2))
                                        ])

    def is_part_of(self, position):
        box = self.data["box_size"] if "box_size" in self.data else (0.5, 0.5, 0.5)
        rpos = self.data["relative_position"] if "relative_position" in self.data else (0, 0, 0)
        mx, my, mz = util.vector.normalize(position)
        sx, sy, sz = mx + box[0] + rpos[0], my + box[1] + rpos[1], mz + box[2] + rpos[2]
        ex, ey, ez = mx - box[0] + rpos[0], my - box[1] + rpos[1], mz - box[2] + rpos[2]
        if sx > ex: ex, sx = sx, ex
        if sy > ey: ey, sy = sy, ey
        if sz > ez: ez, sz = sz, ez
        # print((sx, x, ex), (sy, y, ey), (sz, z, ez))
        return sx <= position[0] <= ex and sy <= position[1] <= ey and sz <= position[2] <= ez


rendering.blockrenderer.IBlockRenderer.ENTRYS[CrossTextureModelEntry.getName()] = CrossTextureModelEntry

