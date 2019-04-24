import globals as G
import texture.ModelHandler
import os


def load_models_from_directory(dir, exclude=[]):
    if not os.path.isdir(dir):
        return
    files = [dir+"/"+x for x in os.listdir(dir)]
    models = []
    while len(files) > 0:
        file = files.pop(0)
        if os.path.isfile(file) and file.endswith(".json") and file not in exclude:
            models.append(G.modelhandler.add_model(file))
        elif os.path.isdir(file) and file not in exclude:
            files += [file + "/" + x for x in os.listdir(file)]
    return models


