import json
import globals as G


def reload_config():
    with open("./config.json") as f:
        G.CONFIG = json.load(f)
        for item in list(G.CONFIG.keys())[:]:
            value = G.CONFIG[item]
            if type(value) == str and not (value.startswith("'") and value.endswith("'")):
                exec(value, G.CONFIG)


reload_config()


def store():
    with open("./config.json") as f:
        orginal = json.load(f)
    new = {}
    for key in orginal.keys():
        value = orginal[key]
        if type(value) == str and not (value.startswith("'") and value.endswith("'")):
            new[key] = value
        else:
            new[key] = G.CONFIG[key]
    with open("./config.json", mode="w") as f:
        json.dump(new, f)

