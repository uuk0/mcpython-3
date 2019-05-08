import rendering.blockrenderer.IBlockRenderer
import util.vertices
import util.vector
import globals as G
import pyglet


class BoxModelEntry(rendering.blockrenderer.IBlockRenderer.IBlockRenderer):
    @staticmethod
    def getName():
        return "cube"

    def show(self, iblock):
        if iblock.shown_data: self.hide(iblock)
        position = iblock.position
        textureatlas = G.textureatlashandler.atlases[self.model.indexes[0][0]]
        x, y, z = position
        area = self.data["box_size"] if "box_size" in self.data else (0.5, 0.5, 0.5)
        rpos = self.data["relative_position"] if "relative_position" in self.data else (0, 0, 0)
        x += rpos[0]
        y += rpos[1]
        z += rpos[2]
        vertex_data = util.vertices.cube_vertices(x, y, z, *area)
        data = []
        for element in self.data["indexes"]:
            data.append(textureatlas.filearray[self.model.indexes[element][1]])
        texture_data = list(util.vertices.tex_coords(*data))
        # create vertex list
        # FIXME Maybe `add_indexed()` should be used instead
        chunk = util.vector.sectorize(position)
        chunkaccess = G.worldaccess.get_active_dimension_access().get_chunk_for(chunk)
        batch = chunkaccess.batch if "enable_alpha" not in self.data or not self.data["enable_alpha"] else \
            chunkaccess.alpha_batch
        shown_data = batch.add(24, pyglet.gl.GL_QUADS, textureatlas.pygletatlas,
                                      ('v3f/static', vertex_data),
                                      ('t2f/static', texture_data))
        self.store_vertex_data(iblock, [shown_data])

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


rendering.blockrenderer.IBlockRenderer.ENTRYS[BoxModelEntry.getName()] = BoxModelEntry
