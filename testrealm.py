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
import time

from pathlib import Path
from selenium import webdriver
from selenium.webdriver.remote.errorhandler import NoSuchElementException
from utils.error_handlers import *
from utils.app_utils import *
from utils.wb_utils import *
from utils.misc import colr
# from requests_html import HTMLSession, AsyncHTMLSession
# from config import *


# ------ G variables ------


# ------ variables ------


# ------ classes ------


# ------ functions --------


# ------ test realm ------
# -- for selenium --
# - bestbuy -
product_link = 'https://www.bestbuy.ca/en-ca/product/nintendo-eshop-5-gift-card-digital-download/14583634'
product_link = 'https://www.bestbuy.ca/en-ca/product/xbox-series-x-1tb-console/14964951'
product_link = 'https://www.bestbuy.ca/en-ca/product/fitbit-ace-2-kids-activity-tracker-small-grape-only-at-best-buy/13888796?icmp=Recos_3across_tp_sllng_prdcts&referrer=PLP_Reco'
cart_link = 'https://www.bestbuy.ca/en-ca/basket'
add_to_cart_xpath = '//*[@id="test"]/button'
login_link = 'https://www.bestbuy.ca/identity/en-ca/signin?tid=5XvfgvshhDS%252BAUwIKYQLdlGyDnspKQWVP6klxCtzlm9zZddU69rdYiEv8%252BKBsX%252FPQLHeKMT5KnTMJ76PcNFNU3bSKXM6TXzLx2zFglD4Nqsn8LkZFF5msu%252FcdviBbQZgYRdcDUj2A1GopOW%252FUZluebfuKb%252FqTSZHuIoJOC8GL%252BzX57o9Vc7X0rhVS9h6FR%252FUXeMKoLKOP7u0dqJMNJuhqdUKggjaVkjgsyOYA6jfvw3XHgbQzZBQblIoQgGPKq6ARgwdU97%252FHk%252BiOP26yKrxzqozPOCSuhNLgkd1T2k87qEFmhLzgUfuAdmn%252Bzgj1F10'
checkout_xpath = '//*[@id="root"]/div/div[4]/div[2]/div/section/div/main/section/section[2]/div[3]/div/a'
# NOTE: remove item button is different per product
removeitem_xpath = '//*[@id="lineitem-7772b2f1-babf-4eb4-9903-a13590a92060"]/div[3]/div[2]/section[1]/div[2]/div[1]/div[2]/div[3]/div[2]/div/div[1]/button'

# - microsoft
product_link = 'https://www.xbox.com/en-ca/configure/942J774TP9JN?ranMID=36509&ranEAID=AKGBlS8SPlM&ranSiteID=AKGBlS8SPlM-Fn51Adsweeh1DmNoEYpTKA&epi=AKGBlS8SPlM-Fn51Adsweeh1DmNoEYpTKA&irgwc=1&OCID=AID2200057_aff_7814_1243925&tduid=%28ir__ro0hjxxclgkf6n9twymcrahqb22xoxjo9kvurmhu00%29%287814%29%281243925%29%28AKGBlS8SPlM-Fn51Adsweeh1DmNoEYpTKA%29%28%29&irclickid=_ro0hjxxclgkf6n9twymcrahqb22xoxjo9kvurmhu00'
add_to_cart_xpath = '//*[@id="PageContent"]/section/div/div/div/div/div/div[3]/button'
removeitem_xpath = '//*[@id="store-cart-root"]/div/div/div/section[1]/div/div/div/div[1]/div/div/div[2]/div[1]/div/button[1]'
cart_link = 'https://www.xbox.com/en-CA/cart'


def customChromeOptions2(options, headless=False):
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


d_options = uc.ChromeOptions()
customChromeOptions2(d_options, headless=True)
d = uc.Chrome(options=d_options)
addToCart(url=product_link, xpath=add_to_cart_xpath, driver=d, ntry=5)
checkOut(cart_url=cart_link, xpath=checkout_xpath, driver=d, ntry=5)
removeItem()
d.quit()


# ------ config test ------
tst_cfg_dict = configReader('config.ini', verbose=True)

d.refresh()
loginBestbuy(url=login_link, driver=d,
             login_email=tst_cfg_dict['bestbuy_id'], login_password=tst_cfg_dict['bestbuy_password'])
d.save_screenshot('./screenshots/sc.png')


url = login_link
driver = d
login_email = tst_cfg_dict['bestbuy_id']
login_password = tst_cfg_dict['bestbuy_password']


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
