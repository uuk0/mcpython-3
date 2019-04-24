import globals as G
import texture.ModelHandler
import traceback
import os


INDICATORS = ["parent"]


class ModelEntry:
    def __init__(self, name):
        self.name = name
        self.build = None

    def __call__(self, *args, **kwargs):
        self.build = args[0]
        return args[0]


ENTRYS = []


def transform_file(raw_file: str) -> str:
    if raw_file.count(":") == 0:
        sp = raw_file.split("/")
        if sp[0] == "blocks":
            return G.local+"/assets/textures/block/"+str(sp[1])+".png"
        return transform_file(G.local+"/assets/textures/"+str(sp[0])+"/"+str(sp[1])+".png")
    path = raw_file.split(":")[0]
    c_file = "/assets/" + path + "/textures/" + raw_file.split(":")[1] + ".png"
    for filestart in [G.local] + [imod.PATH for imod in G.modhandler.mods.values()]:
        if os.path.exists(filestart + c_file):
            return filestart + c_file


cube_all = ModelEntry("block/cube_all")
ENTRYS.append(cube_all)
@cube_all
def transform_cube_all(data, file):
    sp = file.split("/")
    name = file.split("/")[sp.index("models")-1]+":"+sp[-1].split(".")[0]
    file = transform_file(data["textures"]["all"])
    tdata = {"name": name,
             "files": [file],
             "entrys": [{"name": "cube", "indexes": [0, 0, 0, 0, 0, 0]}]
             }
    return texture.ModelHandler.Model(tdata)


leaves = ModelEntry("block/leaves")
ENTRYS.append(leaves)
@leaves
def transform_leaves(data, file):
    model = transform_cube_all(data, file)
    model.data["entrys"][0]["enable_alpha"] = True
    return model


cube_bottom_top = ModelEntry("block/cube_bottom_top")
ENTRYS.append(cube_bottom_top)
@cube_bottom_top
def transform_cube_bottom_top(data, file):
    name = file.split("/")[-4] + ":" + file.split("/")[-1].split(".")[0]
    bottom = transform_file(data["textures"]["bottom"])
    top = transform_file(data["textures"]["top"])
    side = transform_file(data["textures"]["side"])

    tdata = {"name": name,
             "files": [top, bottom, side],
             "entrys": [{"name": "cube", "indexes": [0, 1, 2, 2, 2, 2]}]
             }
    return texture.ModelHandler.Model(tdata)


cube_column = ModelEntry("block/cube_column")
ENTRYS.append(cube_column)
@cube_column
def transform_cube_column(data, file):
    name = file.split("/")[-4] + ":" + file.split("/")[-1].split(".")[0]
    end = transform_file(data["textures"]["end"])
    side = transform_file(data["textures"]["side"])

    tdata = {"name": name,
             "files": [end, side],
             "entrys": [{"name": "log", "front_index": 0, "side_index": 1}]
             }
    return texture.ModelHandler.Model(tdata)


half_slab = ModelEntry('block/half_slab')
ENTRYS.append(half_slab)
@half_slab
def transform_half_slab(data, file):
    name = file.split("/")[-4] + ":" + file.split("/")[-1].split(".")[0]
    bottom = transform_file(data["textures"]["bottom"])
    top = transform_file(data["textures"]["top"])
    side = transform_file(data["textures"]["side"])

    tdata = {"name": name,
             "files": [top, side],
             "entrys": [{"name": "slab", "side": 1, "top": 0}]
             }
    return texture.ModelHandler.Model(tdata)


MISSING_TRANSFORMERS = ["block/cross", "block/stairs", "block/wall_gate_closed", "block/wall_gate_open"
                        "block/outer_stairs", 'block/wall_gate_open', 'block/outer_stairs', 'block/inner_stairs',
                        'block/fence_side', 'block/fence_post', 'block/fence_inventory', 'block/fence_gate_open',
                        'block/fence_gate_closed', 'block/door_top_rh', 'block/door_top', 'block/door_bottom_rh',
                        'block/door_bottom', 'block/inner_stairs', 'block/tinted_cross', "block/grass",
                        'block/farmland', 'block/crop', 'block/block', 'block/grass_path', 'block/fire_floor',
                        'block/fire_side', 'block/fire_side_alt']


# list of parents that are not needed
MISSING_TRANSFORMERS += ['block/upper_slab']


class McTransform(texture.ModelHandler.IModelTransformer):
    def is_possible_a_model_of_these_type(self, data):
        return all([x in data for x in INDICATORS])

    def try_to_load(self, data, file=None):
        parent = data["parent"]
        # print(parent, [x.name == parent for x in ENTRYS])
        if parent in MISSING_TRANSFORMERS:
            return G.modelhandler.models[G.local+"/assets/models/block/missing_texture.json"]
        for entry in ENTRYS:
            if entry.name == parent:
                try:
                    return entry.build(data, file)
                except:
                    traceback.print_exc()
        print("missing transformer definition for '"+str(parent)+"'. (example: "+str(file)+")")
        return G.modelhandler.models[G.local+"/assets/models/block/missing_texture.json"]


texture.ModelHandler.MODELTRANSFORMERS.append(McTransform())

