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
from utils.error_handlers import *
from utils.app_utils import *
from utils.wb_utils import customChromeOptions
# from requests_html import HTMLSession, AsyncHTMLSession

import config


# ------ G variables ------


# ------ variables ------


# ------ classes ------


# ------ functions --------
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


def addToCart(cart_url, xpath, driver, ntry):
    """add to cart function"""
    # -- access website --
    print(f'Accessing url: {cart_url}...', end='')
    try:
        driver.get(cart_url)
        print('success!\n')
    except:
        print('failed!\n')
        raise OpenUrlFail

    # -- add to cart --
    try:
        clickButton(xpath=xpath, driver=driver, ntry=ntry,
                    error_exception=AddToCartFail, msg='Adding to cart...')
    except ButtonClickFail:
        error('Add to car button not found. Program terminated.')


def fillTextbox(xpath, driver,
                value, ntry: int,
                error_exception: Exception, msg: str = 'Filling in text...', verbose=True):
    """"fill a text box"""
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
        raise OpenUrlFail

    # -- log in bestbuy --
    print('Logging in...', end='')
    try:
        fillTextbox(xpath=xpath_id, driver=driver, value=login_email, ntry=5, error_exception=FillInTextFail,
                    msg='Entering login email...', verbose=False)  # user id
    except ElementNotFound:
        error('User email box not found. Program terminated.')
    except FillInTextFail:
        error('User email input fail. Program terminated.')

    try:
        fillTextbox(xpath=xpath_pw, driver=driver, value=login_password, ntry=5, error_exception=FillInTextFail,
                    msg='Entering login password...', verbose=False)  # pw
    except ElementNotFound:
        error('Password box not found. Program terminated.')
    except FillInTextFail:
        error('Password input fail. Program terminated.')

    try:
        clickButton(xpath=xpath_login_btn, driver=driver, ntry=5,
                    error_exception=ButtonClickFail, msg='Logging in...', verbose=False)
    except ElementNotFound:
        error('Log in button not found. Program terminated.')
    except ButtonClickFail:
        error('Clicking log in button fail. Program terminated.')

    try:
        time.sleep(2)
        login_fail = driver.find_element(
            by='xpath', value='//*[@id="x-SignIn"]/div/div/div')
        if login_fail.is_displayed:
            print('failed!')
            raise LoginFail
    except NoSuchElementException:
        print('success!')


def checkOut(url, xpath, driver, ntry):
    """check out"""
    print(f'Locating the checkout page...', end='')
    try:
        # driver.get(url)
        print('success!\n')
    except:
        print('failed!\n')
        raise OpenUrlFail

    # -- checking out --
    try:
        clickButton(xpath=xpath, driver=driver, ntry=ntry,
                    error_exception=AddToCartFail, msg='checking out...')
    except ButtonClickFail:
        error('Check out button not found. Program terminated.')


def removeItem(xpath, driver, ntry):
    """remove item"""
    # -- remove item --
    try:
        clickButton(xpath=xpath, driver=driver, ntry=ntry,
                    error_exception=AddToCartFail, msg='Removing item...')
    except ButtonClickFail:
        error('Remove item button not found. Program terminated.')


# ------ test realm ------
# -- for selenium --
product_link = 'https://www.bestbuy.ca/en-ca/product/nintendo-eshop-5-gift-card-digital-download/14583634'
product_link = 'https://www.bestbuy.ca/en-ca/product/xbox-series-x-1tb-console/14964951'
product_link = 'https://www.xbox.com/en-ca/configure/942J774TP9JN?ranMID=36509&ranEAID=AKGBlS8SPlM&ranSiteID=AKGBlS8SPlM-Fn51Adsweeh1DmNoEYpTKA&epi=AKGBlS8SPlM-Fn51Adsweeh1DmNoEYpTKA&irgwc=1&OCID=AID2200057_aff_7814_1243925&tduid=%28ir__ro0hjxxclgkf6n9twymcrahqb22xoxjo9kvurmhu00%29%287814%29%281243925%29%28AKGBlS8SPlM-Fn51Adsweeh1DmNoEYpTKA%29%28%29&irclickid=_ro0hjxxclgkf6n9twymcrahqb22xoxjo9kvurmhu00'
cart_link = 'https://www.xbox.com/en-CA/cart'


add_to_cart_xpath = '//*[@id="PageContent"]/section/div/div/div/div/div/div[3]/button'
removeitem_xpath = '//*[@id="store-cart-root"]/div/div/div/section[1]/div/div/div/div[1]/div/div/div[2]/div[1]/div/button[1]'


d_options = uc.ChromeOptions()
customChromeOptions(d_options, headless=False)
d = uc.Chrome(options=d_options)
# d.get(product_link)
# d.find_element()
# clickButton(xpath=add_to_cart_xpath, driver=d, ntry=5,
#             error_exception=AddToCartFail, msg='Adding to cart...')
addToCart(url=product_link, xpath=add_to_cart_xpath, driver=d, ntry=5)
d.quit()

login_link = 'https://www.bestbuy.ca/identity/en-ca/signin?tid=5XvfgvshhDS%252BAUwIKYQLdlGyDnspKQWVP6klxCtzlm9zZddU69rdYiEv8%252BKBsX%252FPQLHeKMT5KnTMJ76PcNFNU3bSKXM6TXzLx2zFglD4Nqsn8LkZFF5msu%252FcdviBbQZgYRdcDUj2A1GopOW%252FUZluebfuKb%252FqTSZHuIoJOC8GL%252BzX57o9Vc7X0rhVS9h6FR%252FUXeMKoLKOP7u0dqJMNJuhqdUKggjaVkjgsyOYA6jfvw3XHgbQzZBQblIoQgGPKq6ARgwdU97%252FHk%252BiOP26yKrxzqozPOCSuhNLgkd1T2k87qEFmhLzgUfuAdmn%252Bzgj1F10'
d_options = uc.ChromeOptions()
customChromeOptions(d_options, headless=False)
d = uc.Chrome(options=d_options)
loginBestbuy(url=login_link, driver=d,
             login_email='jzhangc@gmail.com', login_password='26342531')
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
