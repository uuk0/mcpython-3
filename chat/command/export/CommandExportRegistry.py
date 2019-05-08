

class ISubCommand:
    @staticmethod
    def get_prefix():
        raise NotImplementedError()

    @staticmethod
    def execute(line):
        raise NotImplementedError()

    @staticmethod
    def get_help():
        return []


SUBCOMMANDS = []

