'''custom exceptions and error functions'''
# ------ libraries ------
import sys

from utils.misc import colr


# ------ classes ------
class OpenUrlFail(Exception):
    pass


class ElementNotFound(Exception):
    pass


class AddToCartFail(Exception):
    pass


class CheckOutFail(Exception):
    pass


class RemoveItemFail(Exception):
    pass


class ButtonClickFail(Exception):
    pass


class FillInTextFail(Exception):
    pass


class IdFail(Exception):
    pass


class PasswordFail(Exception):
    pass


class LoginFail(Exception):
    pass


# ------ functions --------
def error(message, *lines):
    """stole from: https://github.com/alexjc/neural-enhance"""
    string = "\n{}ERROR: " + message + "{}\n" + \
        "\n".join(lines) + ("{}\n" if lines else "{}")
    print(string.format(colr.RED_B, colr.RED, colr.ENDC))
    sys.exit(2)


def warn(message, *lines):
    """stole from: https://github.com/alexjc/neural-enhance"""
    string = '\n{}WARNING: ' + message + '{}\n' + '\n'.join(lines) + '{}\n'
    print(string.format(colr.YELLOW_B, colr.YELLOW, colr.ENDC))
