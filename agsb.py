#!/usr/bin/env python3
'''
Waterbox
    Mandatory
    [ ] Construct a functional AGSB
    [ ] Logging function
    [ ] Multiple supplier support (walmart, bestbuy, microsoft)
    [ ] Send me an email when successful
    [ ] Support both guest and logged in methods to purchase
    [x] Add headless mode in __name__ == '__main__' block (arg.add, --headless)

    Optional
    [ ] Given product name search for its link
'''

# ------ libraries ------
import argparse
import time
import sys
import shutil  # to delete temp folder

import undetected_chromedriver.v2 as uc
from pathlib import Path

# from requests_html import HTMLSession
# from selenium import webdriver
# from selenium.webdriver.support.ui import Select
# import config


# ------ classes ------
class ElementNotFound(Exception):
    pass


class AddToCartFail(Exception):
    pass


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


def clickButton(xpath, driver, ntry: int, error_exception: Exception, msg: str = 'Clicking button...'):
    """"click a button"""
    click_button_n = 0
    while True:
        print(msg, end='')
        # load and locate add to cart element
        btn_try_count = 0
        while True:
            """wait the button to load"""
            try:
                add_to_cart_btn = driver.find_element('xpath', xpath)
                break
            except:
                time.sleep(2)
                btn_try_count += 1
                if btn_try_count+1 > 10:
                    raise ElementNotFound
                else:
                    continue

        # add to cart
        if add_to_cart_btn.is_displayed() & add_to_cart_btn.is_enabled():
            time.sleep(2)
            add_to_cart_btn.click()
            print('success!')
            break
        else:
            print('failed!')
            click_button_n += 1
            if click_button_n+1 > ntry:
                raise error_exception
            else:
                print(f'Trying again: {click_button_n+1}/{ntry}.')
                time.sleep(2)
                driver.refresh()
            continue


def addToCart(url, xpath, driver, ntry):
    """add to cart function"""
    print(f'Accessing url: {url}...', end='')
    try:
        driver.get(url)
        print('success!\n')
    except:
        print('failed!\n')
        sys.exit(2)

    # -- add to cart --
    clickButton(xpath=xpath, driver=driver, ntry=ntry,
                error_exception=AddToCartFail, msg='Adding to cart...')


# def main():
#     return None


# ------ G variables ------
__VERSION__ = '0.0.1'
AUTHOR = 'Jing Zhang, PhD'
DESCRIPTION = """
{}--------------------------------- Description -------------------------------------------
A Good Shopping Bot
-----------------------------------------------------------------------------------------{}
""".format(colr.YELLOW, colr.ENDC)


# ------ arguments ------
parser = AppArgParser(description=DESCRIPTION,
                      epilog=f'Written by: {AUTHOR}. Current version: {__VERSION__}\n\r',
                      formatter_class=argparse.RawTextHelpFormatter)

parser._optionals.title = f"{colr.CYAN_B}Help options{colr.ENDC}"

parser.add_argument('-p', '--product', type=str,
                    choices=['xsx', 'xss', 'ps5disc', 'ps5digital'],
                    default='xsx',
                    help='str. Product to buy. (Default: %(default)s)')
parser.add_argument('-s', '--supplier', type=str,
                    choices=['bestbuy', 'walmart', 'microsoft'],
                    default='bestbuy',
                    help='str. Supplier. (Default: %(default)s)')
parser.add_argument('-t', '--tries', type=int,
                    default=10,
                    help='str. Maximum number of tries. (Default: %(default)s)')
addBoolArg(parser=parser, name='headless', input_type='flag', default=False,
           help='Run in headless mode. (Default: %(default)s)')

args = parser.parse_args()


# ------ variables ------
headless = args.headless
product = args.product
supplier = args.supplier
ntry = args.tries

if supplier == 'bestbuy':
    add_to_cart_xpath = '//*[@id="test"]/button'
    if product == 'xsx':
        product_link = 'https://www.bestbuy.ca/en-ca/product/14964951'
    elif product == 'xss':
        product_link = 'https://www.bestbuy.ca/en-ca/product/xbox-series-s-512gb-console/14964950'
    elif product == 'ps5disc':
        product_link = 'https://www.bestbuy.ca/en-ca/product/playstation-5-console/14962185'
    else:
        product_link = 'https://www.bestbuy.ca/en-ca/product/playstation-5-digital-edition-console/15689335'
elif supplier == 'walmart':
    """to be completed"""
    add_to_cart_xpath = '/html/body/div[1]/div/div[4]/div/div/div[1]/div[3]/div[2]/div/div[2]/div[2]/div/button[1]'
    if product == 'xsx':
        product_link = ''
    elif product == 'xss':
        product_link = 'https://www.walmart.ca/en/ip/xbox-series-s/6000201790919'
    elif product == 'ps5disc':
        product_link = ''
    else:
        product_link = ''
elif supplier == 'microsoft':
    """to be completed"""
    add_to_cart_xpath = ''
    if product == 'xsx':
        product_link = ''
    elif product == 'xss':
        product_link = 'https://www.walmart.ca/en/ip/xbox-series-s/6000201790919'
    else:
        error('No playstation is sold by Microsoft.', 'Try other suppliers.')


# ------ main -------
if __name__ == '__main__':
    # -- launch broswer --
    print(f'headless mode: {headless}')
    d_options = uc.ChromeOptions()
    customChromeOptions(d_options, headless=headless)
    d = uc.Chrome(options=d_options)

    # -- purchase --
    try:
        addToCart(url=product_link, xpath=add_to_cart_xpath, driver=d,
                  ntry=ntry)
    except ElementNotFound:
        error(
            'Maximum tries reached. No "add to cart" element found. Program terminated.')
    except AddToCartFail:
        error('Maximum tries reached. Add to cart failed.')
    finally:  # quit browser and clean up
        d.quit()
        print('Cleaning up...', end='')
        try:
            shutil.rmtree('./temp/')
            print('done!\n')
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))

    # main()

    # d.get('https://www.bestbuy.ca/en-ca/product/14964951')
    # if headless:
    #     d.save_screenshot('./screenshots/sc.png')
    # else:
    #     time.sleep(3)
