'''
Waterbox
    Mandatory
    [ ] Construct a functional AGSB
    [ ] Logging function
    [ ] Multiple supplier support (walmart, bestbuy, microsoft)
    [ ] Send me an email when successful
    [ ] Support both guest and logged in methods to purchase
    [x] Add headless mode in __name__ == '__main__' block (arg.add, --headless)
    [ ] Handle read only directories

    Optional
    [ ] Given product name search for its link

Ref links:
http://www.michaelfxu.com/tools%20and%20infrastructures/building-a-sniping-bot/
https://github.com/dkkocab/WebSiteBot_PS5/blob/main/WalmartBot_PS5_Digital.py
https://github.com/armindocachada/yeelight-nvidia-rtx-ryzen-stock-checker/blob/main/Buy%20Bot%20-%20RTX%20GPU.ipynb
https://www.browserstack.com/guide/find-element-by-xpath-in-selenium
https://medium.com/analytics-vidhya/how-to-easily-bypass-recaptchav2-with-selenium-7f7a9a44fa9e
'''

# ------ libraries ------
import shutil
import undetected_chromedriver.v2 as uc
import argparse
import sys
import time
import os

from pathlib import Path
from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.remote.errorhandler import NoSuchElementException
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
class ElementNotFound(Exception):
    pass


class AddToCartFail(Exception):
    pass


class FillInTextFail(Exception):
    pass


class LoginFail(Exception):
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


def customChromeOptions(options, headless=False):
    # Create empty profile
    Path('./.temp/chrome_profile').mkdir(parents=True, exist_ok=True)
    Path('./.temp/chrome_profile/First Run').touch()

    # Set options
    if headless:
        options.headless = True
    else:
        options.add_argument('--user-data-dir=./.temp/chrome_profile/')


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
    add_to_cart_n = 0
    while True:
        print('Adding product to cart...', end='')
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
                    error(
                        'Maximum tries reached. No "add to cart" element found. Program terminated.')
                else:
                    continue

        # click
        if add_to_cart_btn.is_displayed() & add_to_cart_btn.is_enabled():
            time.sleep(2)
            add_to_cart_btn.click()
            print('success!')
            break
        else:
            print('failed!')
            add_to_cart_n += 1
            if add_to_cart_n+1 > ntry:
                raise AddToCartFail
            else:
                print(f'Trying again: {add_to_cart_n+1}/{ntry}.')
                time.sleep(2)
                driver.refresh()
            continue

# def clickAddToCartButton(xpath, driver):
#     try:
#         driver.find_element_by_xpath(xpath).click()
#         pass
#     except Exception:
#         time.sleep(5)
#         driver.refresh()
#         clickAddToCartButton(xpath, driver)


# def clickButton(xpath, driver):
#     try:
#         driver.find_element_by_xpath(xpath).click()
#         pass
#     except Exception:
#         time.sleep(1)
#         clickButton(xpath, driver)


# def enterData(field, data, driver):
#     try:
#         driver.find_element_by_xpath(field).send_keys(data)
#         pass
#     except Exception:
#         time.sleep(1)
#         enterData(field, data, driver)


# ------ test realm ------
# -- for selenium --
product_link = 'https://www.bestbuy.ca/en-ca/product/hp-14-laptop-natural-slver-amd-athlon-silver-3050u-256gb-ssd-8gb-ram-windows-10/15371258'
product_link = 'https://www.bestbuy.ca/en-ca/product/xbox-series-x-1tb-console/14964951'

add_to_cart_xpath = '//*[@id="test"]/button'


def clickButton(xpath, driver, ntry: int, error_exception: Exception, msg: str = 'Clicking button...', verbose=True):
    """"click a button"""
    click_button_n = 0
    while True:
        if verbose:
            print(msg, end='')
        # load and locate add to cart element
        btn_try_count = 0
        while True:
            """wait the button to load"""
            try:
                btn_element = driver.find_element('xpath', xpath)
                break
            except:
                time.sleep(2)
                btn_try_count += 1
                if btn_try_count+1 > 10:
                    raise ElementNotFound
                else:
                    continue

        # click
        if btn_element.is_displayed() & btn_element.is_enabled():
            time.sleep(2)
            btn_element.click()
            if verbose:
                print('success!')
            break
        else:
            if verbose:
                print('failed!')
            click_button_n += 1
            if click_button_n+1 > ntry:
                raise error_exception
            else:
                if verbose:
                    print(f'Trying again: {click_button_n+1}/{ntry}.')
                time.sleep(2)
                driver.refresh()
            continue


def addToCart(url, xpath, driver, ntry):
    # -- access website --
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


d_options = uc.ChromeOptions()
customChromeOptions(d_options, headless=False)
d = uc.Chrome(options=d_options)
addToCart(url=product_link, xpath=add_to_cart_xpath, driver=d, ntry=5)
d.quit()


login_link = 'https://www.bestbuy.ca/identity/en-ca/signin?tid=ZSueQsXhRhIch0oXm4ae8rePROmryXd73oprfLuxH0DM1kOXhVQdL006UIBf2MTAhZD0pYRDab%252BqVI7LS73eRK1GmWKbakTti%252BAaJCDJzLcYcaQzkvvRuyWqLRsxMI1VHPMsYnijRzm%252Be8DjsL0ZT8tnDW%252BC%252Fh1PMKSe4y2SA93LjclYlkyibegDz4VaFFnfua%252B8sIbgZawOT%252BZ9muuG77%252BJjxAWb94FD%252BUwrVbS%252BEYvFblFh5JRIlXaNHZwspJOC4FWjxz2NxVLu7BGFx5JZyvEMDuWUF%252B%252B%252BnXF8ZzQ2yiNsaHrPC7UrqVtFDWi4l6btrYNnoHo9EKdxls5dxWHbrvwLnlY7HjnYPdpUKBReGE%252FcKkDqztH6bgYhA2zNFR98U5DnrWc1XV0VsnPSpW7yFDD1oLw20C1oZVOyM08XG%252F6Zz%252F%252B179EJ71XMNsVJc59'
d_options = uc.ChromeOptions()
customChromeOptions(d_options, headless=False)
d = uc.Chrome(options=d_options)
d.get(login_link)
xpath_id, xpath_pw, xpath_login_btn = '//*[@id="username"]', '//*[@id="password"]', '//*[@id="signIn"]/div/button'
login_email = 'j123@test.ca'
login_password = '123zjin'
el = d.find_element(by='xpath', value=xpath_id)


xpath = xpath_id
driver = d


def fillTextbox(xpath, driver,
                value, ntry: int,
                error_exception: Exception, msg: str = 'Filling in text...', verbose=True):
    """"click a button"""
    fill_try_n = 0
    while True:
        if verbose:
            print(msg, end='')
        # load and locate add to cart element
        find_textbox_n = 0
        while True:
            """wait the button to load"""
            try:
                textbox_element = driver.find_element('xpath', xpath)
                break
            except:
                time.sleep(2)
                find_textbox_n += 1
                if find_textbox_n+1 > 10:
                    raise ElementNotFound
                else:
                    continue

        # fill in text
        if textbox_element.is_displayed() & textbox_element.is_enabled():
            time.sleep(2)
            textbox_element.send_keys(value)
            if verbose:
                print('success!')
            break
        else:
            print('failed!')
            fill_try_n += 1
            if fill_try_n+1 > ntry:
                raise error_exception
            else:
                if verbose:
                    print(f'Trying again: {fill_try_n+1}/{ntry}.')
                time.sleep(2)
                driver.refresh()
            continue


def loginBestbuy(url, driver, login_email, login_password):
    """add to cart function"""
    # -- variables --
    xpath_id, xpath_pw, xpath_login_btn = '//*[@id="username"]', '//*[@id="password"]', '//*[@id="signIn"]/div/button'

    # -- access website --
    print(f'Accessing url: {url}...', end='')
    try:
        driver.get(url)
        print('success!\n')
    except:
        print('failed!\n')
        sys.exit(2)

    # -- log in bestbuy --
    print('Logging in...', end='')
    fillTextbox(xpath=xpath_id, driver=driver, value=login_email, ntry=5, error_exception=FillInTextFail,
                msg='Entering login email...', verbose=False)  # user id
    fillTextbox(xpath=xpath_pw, driver=driver, value=login_password, ntry=5, error_exception=FillInTextFail,
                msg='Entering login password...', verbose=False)  # pw
    clickButton(xpath=xpath_login_btn, driver=driver, ntry=5,
                error_exception=AddToCartFail, msg='Logging in...', verbose=False)

    try:
        time.sleep(2)
        login_fail = driver.find_element(
            by='xpath', value='//*[@id="x-SignIn"]/div/div/div')
        if login_fail.is_displayed:
            print('failed!')
            raise LoginFail
    except NoSuchElementException:
        print('success!')


d_options = uc.ChromeOptions()
customChromeOptions(d_options, headless=False)
d = uc.Chrome(options=d_options)
loginBestbuy(url=login_link, driver=d,
             login_email='jzhangc@gmail.com', login_password='26342531')

d.get(login_link)
fillTextbox(xpath=xpath_id, driver=d, value=login_email, ntry=5, error_exception=FillInTextFail,
            msg='Entering login email...', verbose=False)  # user id
fillTextbox(xpath=xpath_pw, driver=d, value=login_password, ntry=5, error_exception=FillInTextFail,
            msg='Entering login password...', verbose=False)  # pw
clickButton(xpath=xpath_login_btn, driver=d, ntry=5,
            error_exception=AddToCartFail, msg='Logging in...', verbose=False)
time.sleep(3)
login_fail = d.find_element(
    by='xpath', value='//*[@id="x-SignIn"]/div/div/div')

d.quit()

# ------ old ------
driver = webdriver.Chrome('./driver/chromedriver')

driver = uc.Chrome()
driver.get('http://www.google.ca/')
time.sleep(5)
search_box = driver.find_element_by_name('q')
search_box.send_keys('ChromeDriver')
search_box.submit()
time.sleep(5)  # Let the user actually see something!
driver.quit()

d.quit()
Path('./.temp').exists()
Path('./.temp').is_dir()
shutil.rmtree(Path('./.temp'))

d.get(product_link)
tst_button = d.find_element('xpath', '//*[@id="test"]/button')
tst_button.is_displayed()
d.find_element('xpath', '//*[@id="test"]/button').click()
d.refresh()
d.quit()

d.get(product_link)
d.save_screenshot('./.temp/sc.png')
