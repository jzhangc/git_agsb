#!/usr/bin/env python3
'''
Waterbox
    Mandatory
    [ ] Construct a functional AGSB
    [x] Logging function
    [ ] Multiple supplier support (walmart, bestbuy, microsoft)
    [ ] Send me an email when successful
    [ ] Support both guest and logged in methods to purchase
    [x] Add headless mode in __name__ == '__main__' block (arg.add, --headless)
    [ ] Handle read only directories

    Optional
    [ ] Given product name search for its link
'''

# ------ libraries ------
import argparse
import shutil  # to delete temp folder
import sys
import time
from pathlib import Path

import undetected_chromedriver.v2 as uc

from utils.app_utils import AppArgParser, addBoolArg, configReader
from utils.error_handlers import (
    AddToCartFail, CheckOutFail, IdFail, LoginFail, OpenUrlFail, PasswordFail, error)
from utils.wb_utils import (
    addToCart, checkOut, customChromeOptions, loginBestbuy)
from utils.misc import colr

# from requests_html import HTMLSession
# from selenium import webdriver
# from selenium.webdriver.support.ui import Select
# import config


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
parser.add_argument('-c', '--config', type=str,
                    default='config.ini',
                    help='str. Config file path. (Default: %(default)s)')
parser.add_argument('-v', '--version', action='version',
                    version=f'Veresion: {__VERSION__}')
addBoolArg(parser=parser, name='headless', input_type='flag', default=False,
           help='Run in headless mode. (Default: %(default)s)')
addBoolArg(parser=parser, name='login_first', input_type='flag', default=True,
           help='If to log in first. (Default: %(default)s)')

args = parser.parse_args()


# ------ initial variables ------
headless = args.headless
product = args.product
supplier = args.supplier
ntry = args.tries
login_first = args.login_first
cfg_dict = configReader(args.config)

if supplier == 'bestbuy':
    cart_link = 'https://www.bestbuy.ca/en-ca/basket'
    login_link = 'https://www.bestbuy.ca/identity/en-ca/signin?tid=5XvfgvshhDS%252BAUwIKYQLdlGyDnspKQWVP6klxCtzlm9zZddU69rdYiEv8%252BKBsX%252FPQLHeKMT5KnTMJ76PcNFNU3bSKXM6TXzLx2zFglD4Nqsn8LkZFF5msu%252FcdviBbQZgYRdcDUj2A1GopOW%252FUZluebfuKb%252FqTSZHuIoJOC8GL%252BzX57o9Vc7X0rhVS9h6FR%252FUXeMKoLKOP7u0dqJMNJuhqdUKggjaVkjgsyOYA6jfvw3XHgbQzZBQblIoQgGPKq6ARgwdU97%252FHk%252BiOP26yKrxzqozPOCSuhNLgkd1T2k87qEFmhLzgUfuAdmn%252Bzgj1F10'
    add_to_cart_xpath = '//*[@id="test"]/button'
    checkout_xpath = '//*[@id="root"]/div/div[4]/div[2]/div/section/div/main/section/section[2]/div[3]/div/a'
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
    cart_link = 'https://www.walmart.ca/cart'
    login_link = 'https://www.walmart.ca/sign-in?from=%2Fen'
    add_to_cart_xpath = '/html/body/div[1]/div/div[4]/div/div/div[1]/div[3]/div[2]/div/div[2]/div[2]/div/button[1]'
    # enter cart first before checking out
    checkout_xpath = '/html/body/div[1]/div/div/div[3]/div[4]/div[3]/div/div[1]/div[11]/div/a/button'
    if product == 'xsx':
        product_link = 'https://www.walmart.ca/en/ip/xbox-series-x/6000201786332?cmpid=AF_CA_1709054_1&utm_source=rakuten&utm_medium=affiliate&utm_campaign=always_on&utm_content=10&utm_id=AF_CA_1709054_1&siteID=AKGBlS8SPlM-QK_GLz28of76UQwD5B9gqA&wmlspartner=AKGBlS8SPlM'
    elif product == 'xss':
        product_link = 'https://www.walmart.ca/en/ip/xbox-series-s/6000201790919'
    elif product == 'ps5disc':
        product_link = ''
    else:
        product_link = ''
elif supplier == 'microsoft':
    """to be completed"""
    cart_link = 'https://www.xbox.com/en-CA/cart'
    add_to_cart_xpath = '//*[@id="PageContent"]/section/div/div/div/div/div/div[3]/button'
    checkout_xpath = '//*[@id="store-cart-root"]/div/div/div/section[2]/div/div/button'
    # placeorder_xpath = '//*[@id="ember1031"]'  # for controller
    # removeitem_xpath = '//*[@id="store-cart-root"]/div/div/div/section[1]/div/div/div/div[1]/div[1]/div/div[2]/div[1]/div/button[1]'  # controller
    if product == 'xsx':
        product_link = 'https://www.xbox.com/en-ca/configure/8wj714n3rbtl?ranMID=24542&ranEAID=jrr8pPQxhfE&ranSiteID=jrr8pPQxhfE-XmpeLyy2I9TgR3Pno2V1Fg&epi=jrr8pPQxhfE-XmpeLyy2I9TgR3Pno2V1Fg&irgwc=1&OCID=AID2200057_aff_7593_1243925&tduid=%28ir__ro0hjxxclgkf6n9twymcrahqb22xo0odkovurmhu00%29%287593%29%281243925%29%28jrr8pPQxhfE-XmpeLyy2I9TgR3Pno2V1Fg%29%28%29&irclickid=_ro0hjxxclgkf6n9twymcrahqb22xo0odkovurmhu00'
    elif product == 'xss':
        # may need to change
        # placeorder_xpath = '//*[@id="ember1033"]  # for xss
        # removeitem_xpath = '//*[@id="store-cart-root"]/div/div/div/section[1]/div/div/div/div[1]/div/div/div[2]/div[1]/div/button[1]'
        product_link = 'https://www.xbox.com/en-ca/configure/942J774TP9JN?ranMID=36509&ranEAID=AKGBlS8SPlM&ranSiteID=AKGBlS8SPlM-Fn51Adsweeh1DmNoEYpTKA&epi=AKGBlS8SPlM-Fn51Adsweeh1DmNoEYpTKA&irgwc=1&OCID=AID2200057_aff_7814_1243925&tduid=%28ir__ro0hjxxclgkf6n9twymcrahqb22xoxjo9kvurmhu00%29%287814%29%281243925%29%28AKGBlS8SPlM-Fn51Adsweeh1DmNoEYpTKA%29%28%29&irclickid=_ro0hjxxclgkf6n9twymcrahqb22xoxjo9kvurmhu00'
    else:
        error('No playstation is sold by Microsoft.', 'Try other suppliers.')


# ------ main -------
if __name__ == '__main__':
    # -- launch browser --
    print(f'headless mode: {headless}\n')
    d_options = uc.ChromeOptions()
    customChromeOptions(d_options, headless=headless)
    d = uc.Chrome(options=d_options)

    # -- log in or not --
    login_except_flag = True
    try:
        if supplier == 'bestbuy':
            loginBestbuy(url=login_link, driver=d,
                         login_email=cfg_dict['bestbuy_id'], login_password=cfg_dict['bestbuy_password'])
        # elif supplier == 'microsoft':
        #     loginMicrosoft(url=login_link, driver=d,
        #                    login_email=cfg_dict['ms_id'], login_password=cfg_dict['ms_password'])
        # else:
        #     loginWalmart(url=login_link, driver=d,
        #                  login_email=cfg_dict['walmart_id'], login_password=cfg_dict['walmart_password'])
        login_except_flag = False
    except PasswordFail:
        error('Incorrect login password.')
    except IdFail:
        error('Incorrect login id.')
    except LoginFail:
        error('Log in failed')
    finally:
        if login_except_flag:  # if any exceptions, exit and do the clean up
            d.quit()
            print('Cleaning up...', end='')
            try:
                shutil.rmtree('./.temp/')
                print('done!\n')
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))

    # -- purchase --
    try:
        addToCart(url=product_link, xpath=add_to_cart_xpath, driver=d,
                  ntry=ntry)
        checkOut(cart_url=cart_link, xpath=checkout_xpath, driver=d, ntry=ntry)
    except OpenUrlFail:
        error('Product URL cannot be reached.')
    except AddToCartFail:
        error('Maximum tries reached. Add to cart failed.')
    except CheckOutFail:
        error('Maximum tries reached. Checkout failed.')
    finally:  # quit browser and clean up
        d.quit()
        print('Cleaning up...', end='')
        try:
            shutil.rmtree('./.temp/')
            print('done!\n')
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
    # if headless:
    #     d.save_screenshot('./screenshots/sc.png')
    # else:
    #     time.sleep(3)
