import sys
from termcolor      import colored, cprint

class Logger:
    @staticmethod
    def Stderr(message, end = '\n', attrs = []):
        cprint(message, end = end, attrs = attrs, file = sys.stderr)
        return 0

    @staticmethod
    def Stdout(message, end = '\n', attrs = []):
        cprint(message, end = end, attrs = attrs, file = sys.stdout)
        return 0

    @staticmethod
    def Error(message, c = 'red', end = '\n', attrs = []):
        cprint(message, c, end = end, attrs = attrs, file = sys.stderr)
        return -1

    @staticmethod
    def Info(message, c = 'blue', end = '\n', attrs = []):
        cprint(message, c, end = end, attrs = attrs, file = sys.stdout)
        return 0

    @staticmethod
    def Warn(message, c = 'yellow', end = '\n', attrs = []):
        cprint(message, c, end = end, attrs = attrs, file = sys.stdout)
        return 1

    @staticmethod
    def Input(message, c = 'magenta', end = '\n', attrs = []):
        cprint('[optional] ' + message, c, end=end,
               attrs=attrs, file=sys.stdout)
        return 0

    @staticmethod
    def Required(message, c = 'red', end = '\n', attrs = []):
        attrs.append('underline')

        cprint('[required] ' + message, c, end=end,
               attrs=attrs, file=sys.stdout)
        return 0

    @staticmethod
    def Success(message, c = 'green', end = '\n', attrs = [ 'bold' ]):
        cprint(message, c, end = end, attrs = attrs, file = sys.stdout)
        return 1

    @staticmethod
    def Failed(message, c = 'red', end = '\n', attrs = [ 'bold' ]):
        cprint(message, c, end=end, attrs=attrs, file=sys.stdout)
        return -1

    @staticmethod
    def Alert(message, c = 'yellow', end = '\n', attrs = []):
        cprint(message, c, end=end, attrs=attrs, file=sys.stdout)
        return 0
