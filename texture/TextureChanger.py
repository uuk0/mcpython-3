import globals as G
import PIL.Image


class TextureChangerHandler:
    def __init__(self):
        self.modes = {}

    def register(self, obj):
        self(obj)

    def __call__(self, *args, **kwargs):
        self.modes[args[0].getName()] = args[0]
        return args[0]

    def generate_textures(self, images, mode: str, *args, **kwargs) -> list:
        if mode not in self.modes:
            raise ValueError("can't access mode "+str(mode))
        return self.modes[mode].generate(images, *args, **kwargs)


G.texturechangerhandler = TextureChangerHandler()


class ITextureChangeAble:
    @staticmethod
    def getName() -> str:
        raise NotImplementedError()

    @staticmethod
    def generate(images, *args, **kwargs) -> list:
        raise NotImplementedError()


@G.texturechangerhandler
class TextureResizeAble(ITextureChangeAble):
    @staticmethod
    def getName() -> str:
        return "resize"

    @staticmethod
    def generate(images, size) -> list:
        results = []
        for image in (images if type(images) in (tuple, list) else [images]):
            results.append(image.resize(size))
        return results


@G.texturechangerhandler
class TextureSplitAble(ITextureChangeAble):
    @staticmethod
    def getName() -> str:
        return "split"

    @staticmethod
    def generate(images, splitsize) -> list:
        results = []
        for image in (images if type(images) in (tuple, list) else [images]):
            sx, sy = image.size
            sx /= splitsize[0]
            sy /= splitsize[1]
            for x in range(splitsize[0]):
                for y in range(splitsize[1]):
                    results.append(image.crop((x*sx, y*sy, x*sx+sx-1, y*sy+sy-1)))
        return results


@G.texturechangerhandler
class TextureTileGetter(ITextureChangeAble):
    TILE_ID = 0

    @staticmethod
    def getName() -> str:
        return "crop"

    @staticmethod
    def generate(images, areas) -> list:
        results = []
        for image in (images if type(images) in (tuple, list) else [images]):
            for area in (areas if type(areas[0]) in (tuple, list) else [areas]):
                im = image.crop(area)
                # im.save(G.local+"/tmp/texture_tile_generated_"+str(TextureTileGetter.TILE_ID)+".png")
                results.append(im)  # G.local+"/tmp/texture_tile_generated_"+str(TextureTileGetter.TILE_ID)+".png")
                TextureTileGetter.TILE_ID += 1
        return results


@G.texturechangerhandler
class TextureRotator(ITextureChangeAble):
    @staticmethod
    def getName() -> str:
        return "rotate"

    @staticmethod
    def generate(images, rotation) -> list:
        results = []
        for image in (images if type(images) in (tuple, list) else [images]):
            results.append(image.rotate(rotation))
        return results

