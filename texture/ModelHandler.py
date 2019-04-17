import globals as G
import texture.TextureAtlas
import json
import util.vertices, util.vector
import pyglet
import os
import PIL.Image
import util.vector
import Block.ILog
import Block.ISlab
import traceback
import modloader.events.LoadStageEvent


class ModelHandler:
    def __init__(self):
        self.models = {}
        self.modelindex = {}
        modloader.events.LoadStageEvent.textureatlas_load("minecraft")(self.generate_atlases)

    def add_model(self, file):
        if file in self.models: return self.models[file]
        with open(file) as f:
            try:
                model = Model(json.load(f))
            except:
                print("error occured during loading file "+str(file))
                # traceback.print_exc()
                return
            self.models[file] = model
            self.modelindex[model.name] = model
        return self.models[file]

    def generate(self):
        m = list(self.models.values())
        for model in m:
            model.generate()

    def generate_atlases(self, *args):
        m = list(self.models.values())
        m.sort(key=lambda model: model.name.split(":")[-1])
        m.sort(key=lambda model: len(model.files), reverse=True)
        for model in m:
            model.create_files()

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

    def get_texture_changes(self, start_index):
        return []


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


class LogModelEntry(IModelEntry):
    @staticmethod
    def getName():
        return "log"

    def __init__(self, *args, **kwargs):
        IModelEntry.__init__(self, *args, **kwargs)
        self.sub_model = BoxModelEntry({}, self.model)
        self.indexes = [self.data["front_index"], self.data["side_index"]]

    def show(self, position):
        self.update_submodel_for(position)
        self.sub_model.show(position)

    def hide(self, position):
        self.update_submodel_for(position)
        self.sub_model.hide(position)

    def update_submodel_for(self, position):
        block = G.model.world[position]
        if issubclass(type(block), Block.ILog.ILog):
            orientation = block.get_rotation()
            if orientation == "UD":
                self.sub_model.data = {"name": "cube", "indexes": [self.indexes[0]]*2+[self.indexes[1]]*4}
            elif orientation == "NS":
                self.sub_model.data = {"name": "cube", "indexes": [self.indexes[1], self.indexes[2]] +
                                                                  [self.indexes[0]]*2 + [self.indexes[2]]*2}
            elif orientation == "OW":
                self.sub_model.data = {"name": "cube", "indexes": [self.indexes[2], self.indexes[1]] +
                                                                  [self.indexes[2]]*2 + [self.indexes[0]]*2}
            else:
                raise ValueError("rotation "+str(orientation)+" is unknown")
        else:
            raise ValueError("position contains block that is not supported")

    def is_part_of(self, position):
        # self.update_submodel_for(position)
        return self.sub_model.is_part_of(position)

    def get_texture_changes(self, start_index):
        self.indexes.append(start_index)
        return [{"type": "rotate",
                 "files": [self.indexes[1]],
                 "arguments": [90]}]


IModelEntry.ENTRYS[LogModelEntry.getName()] = LogModelEntry


class SlabModelEntry(IModelEntry):
    @staticmethod
    def getName():
        return "slab"

    def __init__(self, *args, **kwargs):
        IModelEntry.__init__(self, *args, **kwargs)
        self.sub_model = BoxModelEntry({}, self.model)
        self.indexes = [self.data["side"], self.data["top"]]

    def show(self, position):
        self.update_submodel_for(position)
        self.sub_model.show(position)

    def hide(self, position):
        self.update_submodel_for(position)
        self.sub_model.hide(position)

    def update_submodel_for(self, position):
        block = G.model.world[position]
        if issubclass(type(block), Block.ISlab.ISlab):
            mode = block.get_state()
            if mode == "up":
                self.sub_model.data = {"name": "cube",
                                       "indexes": [self.indexes[1]]*2+[self.indexes[2]]*4,
                                       "box_size": [0.5, 0.25, 0.5],
                                       "relative_position": [0, 0.25, 0]}
            elif mode == "down":
                self.sub_model.data = {"name": "cube",
                                       "indexes": [self.indexes[1]]*2+[self.indexes[3]]*4,
                                       "box_size": [0.5, 0.25, 0.5],
                                       "relative_position": [0, -0.25, 0]}
            elif mode == "double":
                self.sub_model.data = {"name": "cube", "indexes": [self.indexes[1]]*2+[self.indexes[0]]*4}
            else:
                raise ValueError("unknown state of slab: "+str(mode))
        else:
            raise ValueError("position cotains block that is not supported")

    def is_part_of(self, position):
        # self.update_submodel_for(position)
        return self.sub_model.is_part_of(position)

    def get_texture_changes(self, start_index):
        self.indexes += [start_index+1, start_index+3]
        return [{"type": "crop", "files": self.indexes[0], "arguments": [[[0, 0, 15, 7]]]},
                {"type": "resize", "files": start_index, "arguments": [[64, 64]]},
                {"type": "crop", "files": self.indexes[0], "arguments": [[[0, 7, 15, 15]]]},
                {"type": "resize", "files": start_index+2, "arguments": [[64, 64]]}]


IModelEntry.ENTRYS[SlabModelEntry.getName()] = SlabModelEntry


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
                self.texturechanges += self.entrys[-1].get_texture_changes(len(self.files) + len(self.texturechanges))
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
                                                                *element["arguments"] if "arguments" in element else [])
            self.files += results

    def create_files(self):
        self.indexes = G.textureatlashandler.add_images(self.files)
        # print(self.name, self.indexes)


@modloader.events.LoadStageEvent.model_load("minecraft")
def load_models(*args):
    for e in os.listdir(G.local+"/assets/models/block"):
        if os.path.isfile(G.local+"/assets/models/block/"+e):
            G.modelhandler.add_model(G.local+"/assets/models/block/"+e)

