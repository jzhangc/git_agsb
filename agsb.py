'''
Waterbox
[ ] Construct a functional AGSB
[ ] Get product links given product name
[ ] Logging function
[ ] Multiple browser support
[ ] Multiple supplier support (walmart, bestbuy, microsoft)
[ ] Send me a text message when successful

'''

# ------ libraries ------
import argparse
import time

import undetected_chromedriver.v2 as uc
from requests_html import HTMLSession
from selenium import webdriver
from selenium.webdriver.support.ui import Select

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
def tstBuyBestbuy(url, xpath, driver):
    driver.get(url)
    add_to_cart_btn = driver.find_element('xpath', xpath)

    while True:
        driver.refresh()
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


def main():
    return None


# ------ main -------
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AGSB arguments')
    parser.add_argument('--name', required=True,
                        help='Specify product name to find and purchase')
    args = parser.parse_args()

    d = webdriver.Chrome('./driver/chromedriver')
    main()
