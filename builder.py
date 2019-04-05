import zipfile
import os
import sys
import globals as G

EXCLUDE = ["builds", "tmp", "__pycache__", ".idea"]


def build():
    print("mcpython builder is starting")
    print(" -collecting files...")
    files = []
    for (path, dirs, lfiles) in os.walk(G.local):
        files += [os.path.join(path, x) for x in lfiles]
    print(" -generating build-zip")
    with zipfile.ZipFile(G.local+"/builds/build_"+str(G.CONFIG["BUILD"])+".zip", mode="w") as f:
        for file in files:
            if not any([x in file for x in EXCLUDE]):
                f.write(file, os.path.relpath(file, G.local))

