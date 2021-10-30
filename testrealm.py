'''
Waterbox
[ ] Construct a functional AGSB
[ ] Get product links given product name
[ ] Logging function
[ ] Multiple browser support
[ ] Multiple supplier support (walmart, bestbuy, microsoft)
[ ] Send me an email when successful
[ ] Add headless mode in __name__ == '__main__' block
[x] Add headless mode in __name__ == '__main__' block (arg.add, --headless)

Ref links:
http://www.michaelfxu.com/tools%20and%20infrastructures/building-a-sniping-bot/
https://github.com/dkkocab/WebSiteBot_PS5/blob/main/WalmartBot_PS5_Digital.py
https://github.com/armindocachada/yeelight-nvidia-rtx-ryzen-stock-checker/blob/main/Buy%20Bot%20-%20RTX%20GPU.ipynb
https://www.browserstack.com/guide/find-element-by-xpath-in-selenium
https://medium.com/analytics-vidhya/how-to-easily-bypass-recaptchav2-with-selenium-7f7a9a44fa9e
'''

# ------ libraries ------
import undetected_chromedriver.v2 as uc
import argparse
import sys
import time

from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from requests_html import HTMLSession, AsyncHTMLSession

import config

# ------ G variables ------
VERSION = '0.0.1'
SUPPLIER = 'microsoft'
PRODUCT = 'xbox'

XBOX_LINK = ''
PS5_LINK = ''


# ------ variables ------
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

r = HTMLSession()
r = r.get(product_link)


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


def checkOnlineBestbuy(url):
    '''check if available to order online'''
    r = HTMLSession()
    r = r.get(url)

    buy_btn = r.html.find(
        'button[class="button_E6SE9 primary_1oCqK addToCartButton_1op0t addToCartButton regular_1jnnf"]', first=True)

    return (buy_btn is not None)


def clickAddToCartButton(xpath, driver):
    try:
        driver.find_element_by_xpath(xpath).click()
        pass
    except Exception:
        time.sleep(5)
        driver.refresh()
        clickAddToCartButton(xpath, driver)


def clickButton(xpath, driver):
    try:
        driver.find_element_by_xpath(xpath).click()
        pass
    except Exception:
        time.sleep(1)
        clickButton(xpath, driver)


def enterData(field, data, driver):
    try:
        driver.find_element_by_xpath(field).send_keys(data)
        pass
    except Exception:
        time.sleep(1)
        enterData(field, data, driver)


# ------ main -------
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='AGSB arguments')
    parser.add_argument('--name', required=True,
                        help='Specify product name to find and purchase')
    args = parser.parse_args()
    main(target_product=args.name)


# ------ test realm ------
# -- requests_html --
product_link = 'https://www.bestbuy.ca/en-ca/product/hp-14-laptop-natural-slver-amd-athlon-silver-3050u-256gb-ssd-8gb-ram-windows-10/15371258'
product_link = 'https://www.bestbuy.ca/en-ca/product/xbox-series-x-1tb-console/14964951'
r = HTMLSession()
r = r.get(product_link)

buy_btn = r.html.find(
    'button[class="button_E6SE9 primary_1oCqK addToCartButton_1op0t addToCartButton regular_1jnnf"]', first=True)
buy_btn
buy_btn is not None


checkOnlineBestbuy(product_link)


# -- for selenium --
driver = webdriver.Chrome('./driver/chromedriver')

driver = uc.Chrome()
driver.get('http://www.google.ca/')
time.sleep(5)
search_box = driver.find_element_by_name('q')
search_box.send_keys('ChromeDriver')
search_box.submit()
time.sleep(5)  # Let the user actually see something!
driver.quit()


def tstBuyBestbuy(url, xpath, driver):

    print(f'Accessing url: {url}...', end='')
    try:
        driver.get(url)
        print('success!\n')
    except:
        print('failed!\n')
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


d = uc.Chrome()
product_link = 'https://www.bestbuy.ca/en-ca/product/hp-14-laptop-natural-slver-amd-athlon-silver-3050u-256gb-ssd-8gb-ram-windows-10/15371258'
add_to_cart_xpath = '//*[@id="test"]/button'
d.get(product_link)
tst_button = d.find_element('xpath', '//*[@id="test"]/button')
tst_button.is_displayed()
d.find_element('xpath', '//*[@id="test"]/button').click()
d.refresh()
d.quit()

d.quit()


d_options = uc.ChromeOptions()
d_options.user_data_dir = './temp/uc_profile'
d_options.headless = False
d_options.add_argument('--no-default-browser-check')

d = uc.Chrome(options=d_options)
d.get(product_link)
d.save_screenshot('./temp/sc.png')
tstBuyBestbuy(url=product_link, xpath=add_to_cart_xpath, driver=d)
d.quit()

"""
ChromeOptions Options
--disable-default-apps
--disable-extensions
--disable-infobars
--disable-notifications
--disable-password-generation
--disable-password-manager-reauthentication
--disable-password-separated-signin-flow
--disable-popup-blocking
--disable-save-password-bubble
--disable-translate
--incognito
--mute-audio
--no-default-browser-check

"""


d.quit()
