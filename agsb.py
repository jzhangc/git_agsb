#!/usr/bin/env python3
'''
Waterbox
[ ] Construct a functional AGSB
[ ] Get product links given product name
[ ] Logging function
[ ] Multiple browser support
[ ] Multiple supplier support (walmart, bestbuy, microsoft)
[ ] Send me a text message when successful
[x] Add headless mode in __name__ == '__main__' block (arg.add, --headless)
'''

# ------ libraries ------
import argparse
import time
import sys

import undetected_chromedriver.v2 as uc
from pathlib import Path
from requests_html import HTMLSession
from selenium import webdriver
from selenium.webdriver.support.ui import Select

import config


# ------ classes ------
class colr:
    WHITE = '\033[0;97m'
    WHITE_B = '\033[1;97m'
    YELLOW = '\033[0;33m'
    YELLOW_B = '\033[1;33m'
    RED = '\033[0;31m'
    RED_B = '\033[1;31m'
    BLUE = '\033[0;94m'
    BLUE_B = '\033[1;94m'
    CYAN = '\033[0;36m'
    CYAN_B = '\033[1;36m'
    ENDC = '\033[0m'  # end colour


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


def error(message, *lines):
    """
    stole from: https://github.com/alexjc/neural-enhance
    """
    string = "\n{}ERROR: " + message + "{}\n" + \
        "\n".join(lines) + ("{}\n" if lines else "{}")
    print(string.format(colr.RED_B, colr.RED, colr.ENDC))
    sys.exit(2)


def warn(message, *lines):
    """
    stole from: https://github.com/alexjc/neural-enhance
    """
    string = '\n{}WARNING: ' + message + '{}\n' + '\n'.join(lines) + '{}\n'
    print(string.format(colr.YELLOW_B, colr.YELLOW, colr.ENDC))


def customChromeOptions(options, headless=False):
    # Create empty profile
    Path('./temp/chrome_profile').mkdir(parents=True, exist_ok=True)
    Path('./temp/chrome_profile/First Run').touch()

    # Set options
    if headless:
        options.headless = True
    else:
        options.add_argument('--user-data-dir=./temp/chrome_profile/')


def tstBuyBestbuy(url, xpath, driver):
    print(f'Accessing url: {url}...', end='')

    try:
        driver.get(url)
        time.sleep(2)
        print('success!\n')
    except:
        print('failed!')
        sys.exit(2)

    while True:
        btn_try_count = 0
        while True:
            try:
                add_to_cart_btn = driver.find_element('xpath', xpath)
                break
            except:
                time.sleep(2)
                btn_try_count += 1
                if btn_try_count > 10:
                    error(
                        'Maximum tries reached. No add to cart element found. Function terminated.')
                else:
                    continue

        if add_to_cart_btn.is_displayed() & add_to_cart_btn.is_enabled():
            time.sleep(2)
            print('Adding product to cart...', end='')
            time.sleep(2)
            add_to_cart_btn.click()
            # driver.quit()
            print('success!')
            break
        else:
            print('failed!\n')
            time.sleep(2)
            driver.refresh()
            continue


def main():
    return None


# ------ G variables ------
__VERSION__ = '0.0.1'
AUTHOR = 'Jing Zhang, PhD'
DESCRIPTION = """
{}--------------------------------- Description -------------------------------------------
A Good Shopping Bot
-----------------------------------------------------------------------------------------{}
""".format(colr.YELLOW, colr.ENDC)

SUPPLIER = 'microsoft'
PRODUCT = 'xbox'
XBOX_LINK = ''
PS5_LINK = ''


# ------ arguments ------
parser = AppArgParser(description=DESCRIPTION,
                      epilog=f'Written by: {AUTHOR}. Current version: {__VERSION__}\n\r',
                      formatter_class=argparse.RawTextHelpFormatter)

parser._optionals.title = f"{colr.CYAN_B}Help options{colr.ENDC}"

addBoolArg(parser=parser, name='headless', input_type='flag', default=False,
           help='Run in headless mode. (Default: %(default)s)')

args = parser.parse_args()


# ------ variables ------
headless = args.headless

if SUPPLIER == 'microsoft':
    if PRODUCT == 'xbox':
        product_link = "https://www.xbox.com/en-ca/configure/8WJ714N3RBTL?ranMID=36509&ranEAID=AKGBlS8SPlM&ranSiteID=AKGBlS8SPlM-GV4BRGqhq_Am72VVaANyMQ&epi=AKGBlS8SPlM-GV4BRGqhq_Am72VVaANyMQ&irgwc=1&OCID=AID2200057_aff_7814_1243925&tduid=%28ir__lkprzt0gd0kf6j3xn91u1x99af2xrfsfusvurmhu00%29%287814%29%281243925%29%28AKGBlS8SPlM-GV4BRGqhq_Am72VVaANyMQ%29%28%29&irclickid=_lkprzt0gd0kf6j3xn91u1x99af2xrfsfusvurmhu00"
    else:
        product_link = None
elif SUPPLIER == 'bestbuy':
    if PRODUCT == 'xbox':
        product_link = 'https://www.bestbuy.ca/en-ca/product/14964951'
    elif PRODUCT == 'PS5':
        product_link = ''
elif SUPPLIER == 'walmart':
    if PRODUCT == 'xbox':
        product_link = 'https://www.walmart.ca/en/ip/xbox-series-x/6000201786332?cmpid=AF_CA_1709054_1&utm_source=rakuten&utm_medium=affiliate&utm_campaign=always_on&utm_content=10&utm_id=AF_CA_1709054_1&siteID=AKGBlS8SPlM-Jaq2E6vIoIaPd.AS3dXYAg&wmlspartner=AKGBlS8SPlM'
    elif PRODUCT == 'PS5':
        product_link = ''


# ------ main -------
if __name__ == '__main__':
    print(f'head mode: {headless}')
    d_options = uc.ChromeOptions()
    customChromeOptions(d_options, headless=headless)
    d = uc.Chrome(options=d_options)
    if headless:
        d.save_screenshot('./temp/sc.png')

    d.quit()

    # main()
