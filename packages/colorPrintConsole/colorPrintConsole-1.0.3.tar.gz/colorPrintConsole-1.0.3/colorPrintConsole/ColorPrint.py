class ColorPrint:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

    @staticmethod
    def red(text):
        return ColorPrint.RED + text + ColorPrint.RESET

    @staticmethod
    def green(text):
        return ColorPrint.GREEN + text + ColorPrint.RESET

    @staticmethod
    def yellow(text):
        return ColorPrint.YELLOW + text + ColorPrint.RESET

    @staticmethod
    def blue(text):
        return ColorPrint.BLUE + text + ColorPrint.RESET

    @staticmethod
    def magenta(text):
        return ColorPrint.MAGENTA + text + ColorPrint.RESET

    @staticmethod
    def cyan(text):
        return ColorPrint.CYAN + text + ColorPrint.RESET
