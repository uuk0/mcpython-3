import globals as G
import modloader.IMod
import modloader.events.ILoadStageEvent
import os
import zipfile
import importlib
import sys
import json
import modloader.ModVersionParser
import util.sorting
import modloader.IMod
import traceback


class ModHandler:
    def __init__(self):
        self.mods = {}
        self.stages = {}
        self.PATHS = [G.local+"/mods"]
        self.active_mod_data = None
        self.modorder = []

    def search_for_mods(self):
        mod_dirs = []
        mod_c_dirs = []
        for path in self.PATHS:
            if os.path.isdir(path):
                if os.path.isfile(path+"/mod.json"):
                    mod_dirs.append(path)
                else:
                    for spath in os.listdir(path):
                        if os.path.isdir(path+"/"+spath):
                            if os.path.isfile(path+"/"+spath+"/mod.json"):
                                mod_dirs.append(path+"/"+spath)
                        # elif zipfile.is_zipfile(path+"/"+spath):
                        #     mod_c_dirs.append(path+"/"+spath)
            # elif zipfile.is_zipfile(path):
            #     mod_c_dirs.append(path)
        for path in mod_dirs:
            with open(path+"/mod.json") as f:
                self.active_mod_data = [path, json.load(f)]
            sys.path.append(path)
            for modlocation in self.active_mod_data[1]["modloactions"]:
                importlib.import_module(modlocation)
        for path in mod_c_dirs:
            with zipfile.ZipFile(path, mode="r") as zpath:
                with zpath.open("mod.info", mode="r") as f:
                    self.active_mod_data = [path, json.load(f)]
            sys.path.append(path)
            for modlocation in self.active_mod_data[1]["modloactions"]:
                importlib.import_module(modlocation)
        if len(self.mods) == 0: return
        print("found "+str(len(self.mods))+" mods. analysing " + ("them" if len(self.mods) > 1 else "it") + "...")
        depend_error = False
        for imod in self.mods.values():
            info_header = False
            for modinfo in imod.getDependencies():
                if modinfo.count("|") == 2:
                    modname, version_info = tuple(modinfo.split("|"))
                else:
                    modname = modinfo; version_info = "any"
                if modname not in self.mods:
                    depend_error = True
                    if not info_header:
                        print("\nMOD "+str(imod.getDisplayName()))
                        info_header = True
                    print(" -dependencie error: need mod "+str(modname)+" with version info " +
                          modloader.ModVersionParser.get_info(version_info))
                elif version_info != "any":
                    imod_other = self.mods[modname]
                    if not modloader.ModVersionParser.is_valid(version_info, imod_other.getVersion()):
                        depend_error = True
                        if not info_header:
                            print("\nMOD " + str(imod.getDisplayName()))
                            info_header = True
                        print(" -dependencie error: need mod " + str(modname) + " with version info " +
                              modloader.ModVersionParser.get_info(version_info) + ", but getted " +
                              str(imod_other.getVersion()))
            for modinfo in imod.getIncompatibls():
                if modinfo.count("|") == 2:
                    modname, version_info = tuple(modinfo.split("|"))
                else:
                    modname = modinfo; version_info = "any"
                if modname in self.mods:
                    imod_other = self.mods[modname]
                    if modloader.ModVersionParser.is_valid(version_info, imod_other.getVersion()):
                        depend_error = True
                        if not info_header:
                            print("\nMOD " + str(imod.getDisplayName()))
                            info_header = True
                        print(" -dependencie error: is incompatible with mod " + str(modname) + " with version info " +
                              imod_other.getVersion() + ", expected " +
                              str(modloader.ModVersionParser.get_info(version_info)))
        if depend_error:
            print("\nout of the above reasons, the game can't be started")
            sys.exit(-1)

        print("sorting them...")

        mods = list(self.mods.values())
        mods.sort(key=lambda imod: imod.getName())

        depend_info = {}

        for imod in mods:
            depend_info[imod.getName()] = []
            for modname in imod.getDependencies():
                if modname not in imod.getDepends():
                    depend_info[imod.getName()].append(modname)

        for imod in mods:
            for modname in imod.getOptionalDependencies():
                if modname in depend_info:
                    depend_info[imod.getName()].append(modname)
            for modname in imod.getDepends():
                if modname in depend_info:
                    depend_info[modname].append(imod.getName())

        print("sorting them after phases & after dependencies")

        phases = [modloader.IMod.LoadMode.PRE_PRE, modloader.IMod.LoadMode.PRE, modloader.IMod.LoadMode.PRE_POST,
                  modloader.IMod.LoadMode.MIDDLE_PRE, modloader.IMod.LoadMode.MIDDLE,
                  modloader.IMod.LoadMode.MIDDLE_POST, modloader.IMod.LoadMode.POST_PRE, modloader.IMod.LoadMode.POST,
                  modloader.IMod.LoadMode.POST_POST]

        phases_map = {}
        for key in phases: phases_map[key] = []

        for modname in util.sorting.topological_sort([(x, depend_info[x]) for x in depend_info.keys()]):
            imod = self.mods[modname]
            phases_map[imod.getLoadMode()].append(imod)

        print("the following order will be loaded:")
        for phase in phases:
            for imod in phases_map[phase]:
                print(" -"+str(imod.getDisplayName()))

        for phase in phases:
            self.modorder += phases_map[phase]

        for imod in self.modorder:
            imod.on_load()

    def post_loading_phase(self, name, *args, **kwargs):
        print("loading stage "+str(name))
        if name not in self.stages:
            raise ValueError("unknown stage "+str(name))
        stage = self.stages[name]
        mc_inited = False
        for imod in self.modorder:
            if not imod.getLoadMode().startswith("loadmode:pre") and not mc_inited and "minecraft" in stage.tasks:
                for func in stage.tasks["minecraft"]:
                    func(name, *args, **kwargs)
                mc_inited = True
            if imod.getName() in stage.tasks:
                for func in stage.tasks[imod.getName()]:
                    func(name, *args, **kwargs)

    def register(self, element):
        self(element)

    def __call__(self, *args, **kwargs):
        try:
            if issubclass(args[0], modloader.IMod.IMod):
                self.mods[args[0].getName()] = args[0]
                args[0].PATH = self.active_mod_data[0]
                return args[0]
        except TypeError:
            pass
        if type(args[0]) == modloader.events.ILoadStageEvent.ILoadStageEvent:
            self.stages[args[0].name] = args[0]
            return args[0]
        elif len(args) > 0 or not args[0]:
            raise ValueError("can't register object "+str(args[0]))
        else:
            raise ValueError("ModHandler needs something to notate, not nothing")


G.modhandler = ModHandler()

