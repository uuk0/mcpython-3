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
import texture.TextureChanger


class IModelTransformer:
    def is_possible_a_model_of_these_type(self, data):
        raise NotImplementedError()

    def try_to_load(self, data, file=None):
        return False


MODELTRANSFORMERS = []


class ModelHandler:
    def __init__(self):
        self.models = {}
        self.modelindex = {}
        modloader.events.LoadStageEvent.textureatlas_load("minecraft")(self.generate_atlases)

    def add_model(self, file):
        if file in self.models: return self.models[file]
        with open(file) as f:
            data = json.load(f)
            try:
                model = Model(data)
            except:
                for imodeltransformer in MODELTRANSFORMERS:
                    # print(imodeltransformer)
                    if imodeltransformer.is_possible_a_model_of_these_type(data):
                        try:
                            model = imodeltransformer.try_to_load(data, file)
                            if model:
                                self.models[file] = model
                                self.modelindex[model.name] = model
                                # print(model.data)
                                return model
                        except:
                            traceback.print_exc()
                print("error occured during loading file "+str(file))
                # traceback.print_exc()
                return
            self.models[file] = model
            self.modelindex[model.name] = model
        return model

    def generate(self):
        m = list(self.models.values())
        for model in m:
            model.generate()
        for model in m:
            model.create_files()

    def generate_atlases(self, *args):
        m = list(self.models.values())
        m.sort(key=lambda model: model.name.split(":")[-1])
        m.sort(key=lambda model: len(model.files), reverse=True)
        for model in m:
            model.create_files()
            # print(model.files)

    def show(self, block):
        # block = G.model.world[position]
        file = block.get_model_name()
        if file not in self.modelindex or \
                block.get_active_model_index() >= len(self.modelindex[block.get_model_name()].entrys):
            # print(self.modelindex)
            # print(self.modelindex["minecraft:missing_texture"].entrys)
            self.modelindex["minecraft:missing_texture"].entrys[0].show(block)
        else:
            try:
                self.modelindex[block.get_model_name()].entrys[block.get_active_model_index()].show(block)
            except KeyError:
                self.modelindex["minecraft:missing_texture"].entrys[0].show(block)
                print("block", block, "has an texture exception")

    def hide(self, block):
        # block = G.model.world[position]
        file = block.get_model_name()
        if file not in self.modelindex:
            self.modelindex["minecraft:missing_texture"].entrys[0].hide(block)
        else:
            self.modelindex[block.get_model_name()].entrys[block.get_active_model_index()].hide(block)


G.modelhandler = ModelHandler()


import rendering.blockrenderer.IBlockRenderer
from rendering.blockrenderer import (Box, Log, Slab, Cross, IMultiRender)


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
            if entry["name"] in rendering.blockrenderer.IBlockRenderer.ENTRYS:
                self.entrys.append(rendering.blockrenderer.IBlockRenderer.ENTRYS[entry["name"]](entry, self))
                self.texturechanges += self.entrys[-1].get_texture_changes(len(self.files) + len(self.texturechanges))
            else:
                raise ValueError("can't cast model entry data " + str(entry) + " to an model entry")
        for iblockrenderer in self.entrys:
            iblockrenderer.on_create()
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


for e in os.listdir(G.local+"/assets/models/block"):
    if os.path.isfile(G.local+"/assets/models/block/"+e):
        @modloader.events.LoadStageEvent.model_load("minecraft", "loading "+str(e.split(".")[0])+"-model",
                                                    arguments=[e])
        def load_file(eventname, filename):
            G.modelhandler.add_model(G.local+"/assets/models/block/"+filename)

