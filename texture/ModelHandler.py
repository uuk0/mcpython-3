import globals as G
import texture.TextureAtlas
import json
import util.vertices, util.vector
import pyglet
import os
import PIL.Image
import util.vector


class ModelHandler:
    def __init__(self):
        self.models = {}
        self.modelindex = {}

    def add_model(self, file):
        if file in self.models: return self.models[file]
        with open(file) as f:
            try:
                model = Model(json.load(f))
            except:
                print(file)
                raise
            self.models[file] = model
            self.modelindex[model.name] = model
        return self.models[file]

    def generate(self):
        for model in self.models.values():
            model.generate()

    def show(self, position):
        block = G.model.world[position]
        file = block.get_model_name()
        if file not in self.modelindex:
            self.modelindex["minecraft:missing_texture"].entrys[0].show(position)
        else:
            self.modelindex[block.get_model_name()].entrys[block.get_active_model_index()].show(position)

    def hide(self, position):
        block = G.model.world[position]
        file = block.get_model_name()
        if file not in self.modelindex:
            self.modelindex["minecraft:missing_texture"].entrys[0].hide(position)
        else:
            self.modelindex[block.get_model_name()].entrys[block.get_active_model_index()].hide(position)


G.modelhandler = ModelHandler()


class IModelEntry:
    ENTRYS = {}

    def __init__(self, entrydata, model):
        self.data = entrydata
        self.model = model

    @staticmethod
    def getName():
        return ""

    def show(self, position):
        pass

    def hide(self, position):
        pass

    def is_part_of(self, position):
        return True


class BoxModelEntry(IModelEntry):
    @staticmethod
    def getName():
        return "cube"

    def show(self, position):
        if position in G.model._shown: self.hide(position)
        block = G.model.world[position]
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
        batch = G.model.batch if "enable_alpha" not in self.data or not self.data["enable_alpha"] else \
            G.model.alpha_batch
        G.model._shown[position] = batch.add(24, pyglet.gl.GL_QUADS, textureatlas.pygletatlas,
                                               ('v3f/static', vertex_data),
                                               ('t2f/static', texture_data))

    def hide(self, position):
        if position not in G.model._shown: return
        G.model._shown.pop(position).delete()

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


IModelEntry.ENTRYS[BoxModelEntry.getName()] = BoxModelEntry


class Model:
    def __init__(self, data):
        self.data = data
        self.files = data["files"]
        self.indexes = []
        self.entrys = []
        self.name = data["name"]
        self.texturechanges = data["changes"] if "changes" in data else []

    def generate(self):
        for entry in self.data["entrys"]:
            if entry["name"] in IModelEntry.ENTRYS:
                self.entrys.append(IModelEntry.ENTRYS[entry["name"]](entry, self))
            else:
                raise ValueError("can't cast model entry data " + str(entry) + " to an model entry")
        for element in self.texturechanges:
            name = element["type"]
            files = element["files"]
            if type(files) in [str, int]: files = [files]
            images = []
            for file in files:
                if type(file) == str:
                    images.append(PIL.Image.open(file))
                elif type(file) == int:
                    images.append(PIL.Image.open(self.files[file]) if type(self.files[file]) == str else
                                  self.files[file])
            results = G.texturechangerhandler.generate_textures(images, str(name),
                                                                *element["arguments"])
            self.files += results
        self.indexes = G.textureatlashandler.add_images(self.files)
        # print(self.name, self.indexes)


for e in os.listdir(G.local+"/assets/models/block"):
    if os.path.isfile(G.local+"/assets/models/block/"+e):
        G.modelhandler.add_model(G.local+"/assets/models/block/"+e)

