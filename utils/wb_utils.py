'''utilities operating websites'''

# ------ libraries ------
import time
from pathlib import Path

from selenium.webdriver.remote.errorhandler import NoSuchElementException
from fake_useragent import UserAgent
from utils.error_handlers import *


# ------ functions --------
def customChromeOptions(options, headless=False):
    # Create empty profile
    Path('./.temp/chrome_profile').mkdir(parents=True, exist_ok=True)
    Path('./.temp/chrome_profile/First Run').touch()

    # user agent
    ua = UserAgent()
    current_agent = ua.random

    # Set options
    if headless:
        # options.headless = True
        # options.add_argument('--disable-gpu')
        options.add_argument('--headless')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--no-sandbox')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-setuid-sandbox')
        options.add_argument('--disable-blink-features=AutomationControlled')
        # options.add_argument('--user-data-dir=./.temp/chrome_profile/')
        # options.add_argument(f'user-agent={current_agent}')

    options.add_argument('--user-data-dir=./.temp/chrome_profile/')
    options.add_argument(f'user-agent={current_agent}')


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
    """add to cart function"""
    # -- access website --
    print(f'Accessing url: {url}...', end='')
    try:
        driver.get(url)
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


def checkOut(cart_url, xpath, driver, ntry):
    """check out"""
    print(f'Locating cart page...', end='')
    try:
        driver.get(cart_url)
        print('success!\n')
    except:
        print('failed!\n')
        raise OpenUrlFail

    # -- checking out --
    try:
        clickButton(xpath=xpath, driver=driver, ntry=ntry,
                    error_exception=CheckOutFail, msg='checking out...')
    except ButtonClickFail:
        error('Checkout button not found. Program terminated.')


def removeItem(cart_url, xpath, driver, ntry):
    """remove item"""
    print(f'Locating cart page...', end='')
    try:
        driver.get(cart_url)
        print('success!\n')
    except:
        print('failed!\n')
        raise OpenUrlFail

    # -- remove item --
    try:
        clickButton(xpath=xpath, driver=driver, ntry=ntry,
                    error_exception=RemoveItemFail, msg='Removing item...')
    except ButtonClickFail:
        error('Remove item button not found. Program terminated.')


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
            textbox_element.clear()
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


def loginBestbuy(url, driver, login_email, login_password, url_verbose=False):
    """add to cart function"""
    # -- variables --
    xpath_id, xpath_pw, xpath_login_btn = '//*[@id="username"]', '//*[@id="password"]', '//*[@id="signIn"]/div/button'

    # -- access website --
    if url_verbose:
        print(f'Open url {url}...', end='')
    try:
        driver.get(url)
        if url_verbose:
            print('success!\n')
    except:
        if url_verbose:
            print('failed!\n')
        raise OpenUrlFail

    # -- log in bestbuy --
    print('Logging in bestbuy...', end='')

    # -- id and pw --
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

    pw_fail = driver.find_element(
        by='xpath', value='//*[@id="signIn"]/fieldset/div[2]/div/div[2]')
    email_fail = driver.find_element(
        by='xpath', value='//*[@id="signIn"]/fieldset/div[1]/div/div[2]')

    if pw_fail.is_displayed():
        print('failed')
        raise PasswordFail

    time.sleep(1)  # need this for the below to work
    if email_fail.is_displayed():
        print('failed!')
        raise IdFail

    # -- log in --
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
        if login_fail.is_displayed():
            print('failed!')
            raise LoginFail

    except NoSuchElementException:
        print('success!')
