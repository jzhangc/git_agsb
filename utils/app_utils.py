'''utilities for the comamndline app'''

# ------ libraries ------
import argparse
import sys
import os
import configparser


from utils.error_handlers import error, warn
from utils.misc import colr
from tqdm import tqdm


# ------ classes ------
class AppArgParser(argparse.ArgumentParser):
    """
    # Purpose
        The help page will display when (1) no argumment was provided, or (2) there is an error
    """

    def error(self, message, *lines):
        string = "\n{}ERROR: " + message + "{}\n" + \
            "\n".join(lines) + ("{}\n" if lines else "{}")
        print(string.format(colr.RED_B, colr.RED, colr.ENDC))
        self.print_help()
        sys.exit(2)


# ------ functions --------
def addBoolArg(parser, name, help, input_type, default=False):
    """
    # Purpose\n
        Automatically add a pair of mutually exclusive boolean arguments to the
        argparser
    # Arguments\n
        parser: a parser object.\n
        name: str. the argument name.\n
        help: str. the help message.\n
        input_type: str. the value type for the argument\n
        default: the default value of the argument if not set\n
    """
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('--' + name, dest=name,
                       action='store_true', help=input_type + '. ' + help)
    group.add_argument('--no-' + name, dest=name,
                       action='store_false', help=input_type + '. ''(Not to) ' + help)
    parser.set_defaults(**{name: default})


def configReader(config_file, verbose=False):
    """config reader"""
    cfg = configparser.ConfigParser()
    out_dict = {}
    configfile_dir = os.path.normpath(os.path.abspath(
        os.path.expanduser(config_file)))

    try:
        with open(configfile_dir) as f:
            cfg.read(os.path.normpath(os.path.abspath(
                os.path.expanduser(config_file))))
    except FileNotFoundError:
        error(
            f'Config file not found.', 'Check path and try again.')
    except Exception:
        error(f'Config find found but failed to load.')

    for section in tqdm(cfg.sections()):
        for option in cfg.options(section):
            if verbose:
                print(f'Reading {option} from {section}')
            try:
                out_dict[option] = cfg.get(section, option)
            except:
                warn(
                    f'Reading config: {option} error. Setting {option} to None.')
                out_dict[option] = None

    return out_dict
