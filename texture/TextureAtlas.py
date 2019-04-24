import globals as G
import PIL.Image
import util.file
import pyglet
import modloader.ResourceLocator
import modloader.ResourceLocator


class TextureAtlasHandler:
    def __init__(self):
        self.atlases = []

    def generate(self):
        for atlas in self.atlases:
            atlas.generate()

    def add_images(self, files):
        """
        adds all files to one image atlas
        :param files: the files to add
        :return: an indexlist for local atlas indexes
        """
        files = [util.file.normalize(x) if type(x) == str else x for x in files]
        for textureatlas in self.atlases:
            need = textureatlas.calculate_needed_space_for_files(files)
            if need <= textureatlas.free_places:
                return [(textureatlas.id, x) for x in textureatlas.add_files(files)]
        textureatlas = TextureAtlas(len(self.atlases))
        self.atlases.append(textureatlas)
        return [(textureatlas.id, x) for x in textureatlas.add_files(files)]


G.textureatlashandler = TextureAtlasHandler()


class TextureAtlas:
    def __init__(self, id):
        self.id = id
        self.free_places = 256
        self.filearray = {}  # id -> texture atlas index
        self.indexarray = {}  # id -> file
        self.fileindexarray = {}  # file -> id
        self.pygletatlas = None
        self.maxsize = [64, 64]

    def generate(self):
        iindex = [0, 0]
        image = PIL.Image.new("RGBA", (16*self.maxsize[0], 16*self.maxsize[1]))
        for file in self.indexarray.values():
            if type(file) == str:
                index = self.fileindexarray[file]
                resourcelocator = modloader.ResourceLocator.ResourceLocation(file)
                source = resourcelocator.load_as_image()
            else:
                source = file[0]
                index = file[1]
            if source.size[0] / self.maxsize[0] == source.size[1] / self.maxsize[1]:
                source = source.resize(self.maxsize)
            image.paste(source, (iindex[0]*self.maxsize[0], (15-iindex[1])*self.maxsize[1]))
            self.filearray[index] = tuple(iindex)
            iindex[0] += 1
            if iindex[0] > 15:
                iindex[0] = 0
                iindex[1] += 1
        image.save(G.local+"/tmp/imageatlas_"+str(self.id)+".png")
        self.pygletatlas = pyglet.graphics.TextureGroup(
            pyglet.image.load(G.local+"/tmp/imageatlas_"+str(self.id)+".png").texture)

    def add_files(self, files):
        """
        adds the files to the system
        :return: the indexes needed to access it
        """
        indexes = []
        for file in files:
            if type(file) == PIL.Image.Image:
                image = file
            else:
                rlocator = modloader.ResourceLocator.ResourceLocation(file)
                image = rlocator.load_as_image()
            if image.size[0] > self.maxsize[0]: self.maxsize[0] = image.size[0]
            if image.size[1] > self.maxsize[1]: self.maxsize[1] = image.size[1]
            if type(file) == PIL.Image.Image:
                self.free_places -= 1
                index = len(self.indexarray)
                indexes.append(index)
                self.indexarray[index] = [file, index]
            elif file in self.fileindexarray and type(file) == str:
                indexes.append(self.fileindexarray[file])
            else:
                self.free_places -= 1
                index = len(self.indexarray)
                indexes.append(index)
                self.fileindexarray[file] = index
                self.indexarray[index] = file if type(file) == str else [file, index]
        return indexes

    def calculate_needed_space_for_files(self, files):
        need = len(files)
        for file in files:
            if type(file) == str and file in self.fileindexarray:
                need -= 1
        return need

