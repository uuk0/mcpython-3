import globals as G
import os


def normalize(file):
    if os.path.isfile(file): return file
    if os.path.isfile(os.path.join(G.local, file)): return os.path.join(G.local, file)
    print(file, os.path.join(G.local, file))
    return file

