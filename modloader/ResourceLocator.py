import globals as G
import os
import zipfile
import PIL.Image
import json


class LocationConfig:
    FILEENDINGS = [".png", ".json"]

    class Format1:
        LTYPEPREFIXES = ["textures"]


class ResourceLocation:
    def __init__(self, location):
        self.location = location
        self.is_ziped = False
        if os.path.exists(location):
            self.path = location
            self.is_ziped = False
        else:
            if location.count(":") and location.count("/") == 1:
                # format 1
                modname = location.split(":")[0]
                old = location.split(":")[1]
                ltype = old.split("/")[0]
                address = old.split("/")[1]
                imod = G.modhandler.mods[modname]
                path = imod.PATH
                self.subpath = path
                if zipfile.is_zipfile(path):
                    self.is_ziped = False
                else:
                    self.is_ziped = False  # True

                for spre in LocationConfig.Format1.LTYPEPREFIXES:
                    for fending in LocationConfig.FILEENDINGS:
                        cpath = "assets/"+spre+"/"+ltype+"/"+address+fending
                        if os.path.exists(path+"/"+cpath):
                            self.sub_location = cpath
                            break
                        elif self.is_ziped:
                            with zipfile.ZipFile(path) as f:
                                try:
                                    f.getinfo(cpath)
                                    self.sub_location = cpath
                                    break
                                except KeyError:
                                    pass

                self.path = path + "/" + self.sub_location
            else:
                flag = False
                # print(G.modhandler.mods, [imod.PATH for imod in G.modhandler.mods.values()])
                for imod in G.modhandler.mods.values():
                    path = imod.PATH + "/" + location
                    if os.path.exists(path) and not flag:
                        self.path = imod.PATH + "/" + location
                        flag = True
                if os.path.exists(G.local + "/" + location) and not flag:
                    self.path = G.local + "/" + location
                    flag = True
                elif not flag:
                    raise ValueError("unknown format "+str(location))
                self.is_ziped = False

    def load_as_image(self):
        if self.is_ziped:
            with zipfile.ZipFile(self.subpath) as f:
                f.extract(self.sub_location, G.local+"/tmp/resourceloactor_tmp.png")
            return PIL.Image.open(G.local+"/tmp/resourceloactor_tmp.png")
        else:
            return PIL.Image.open(self.path)

    def load_as_json(self):
        if self.is_ziped:
            with zipfile.ZipFile(self.subpath) as f:
                with f.open(self.sub_location) as sf:
                    json.load(sf)
        else:
            with open(self.path) as f:
                return json.load(f)

