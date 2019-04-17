

class LoadMode:
    """
    Enum for diffrent load parts for Mods. First in list -> first inited
    """

    PRE_PRE = "loadmode:pre:pre"
    PRE = "loadmode:pre"
    PRE_POST = "loadmode:pre:post"

    MIDDLE_PRE = "loadmode:middle:pre"
    MIDDLE = "loadmode:middle"
    MIDDLE_POST = "loadmode:middle:post"

    POST_PRE = "loadmode:post:pre"
    POST = "loadmode:post"
    POST_POST = "loadmode:post:post"


class IMod:
    PATH = None

    @staticmethod
    def on_load():
        pass

    @staticmethod
    def getName():
        raise NotImplementedError()

    @classmethod
    def getDisplayName(cls):
        return cls.getName()

    @staticmethod
    def getVersion():
        return "0.0.0"

    @classmethod
    def getModPrefix(cls):
        return cls.getName().lower()

    @staticmethod
    def getDependencies():
        return []

    @staticmethod
    def getOptionalDependencies():
        return []

    @staticmethod
    def getIncompatibls():
        return []

    @staticmethod
    def getDepends():
        return []

    @staticmethod
    def getLoadMode():
        return LoadMode.MIDDLE

    @staticmethod
    def getVersionID():
        return -1

    @classmethod
    def is_valid_version(cls, version):
        return cls.convert_info_to_ID(version) == cls.getVersionID()

    @staticmethod
    def convert_info_to_ID(info):
        return -1

