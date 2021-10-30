'''
Waterbox
[ ] Construct a functional AGSB
[ ] Get product links given product name
[ ] Logging function
[ ] Multiple browser support
[ ] Multiple supplier support (walmart, bestbuy, microsoft)
[ ] Send me a text message when successful

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


import time

from selenium import webdriver
from selenium.webdriver.support.ui import Select
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


# ------ functions --------
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


driver = uc.Chrome()
product_link = 'https://www.bestbuy.ca/en-ca/product/hp-14-laptop-natural-slver-amd-athlon-silver-3050u-256gb-ssd-8gb-ram-windows-10/15371258'
driver.get(product_link)
tst_button = driver.find_element('xpath', '//*[@id="test"]/button')
tst_button.is_displayed()
driver.find_element('xpath', '//*[@id="test"]/button').click()
driver.quit()


def tstBuyBestbuy(url, driver):
    driver.get(url)

    while True:
        add_to_cart_btn = driver.find_element(
            'xpath', '//*[@id="test"]/button')

        print(f'Accessing url: {url}...', end='')
        if add_to_cart_btn.is_displayed() & add_to_cart_btn.is_enabled():
            time.sleep(2)
            print('success!\n')
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
            continue


d = uc.Chrome()
tstBuyBestbuy(url=product_link, driver=d)
d.quit()
