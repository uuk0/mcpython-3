import globals as G


class ICommand:
    @staticmethod
    def get_prefix(): raise NotImplementedError()

    @staticmethod
    def get_syntax(): return []

    @staticmethod
    def execute_command(line, parsed_values): raise NotImplementedError()

    @staticmethod
    def get_help_lines(): return []

