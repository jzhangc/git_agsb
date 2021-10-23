'''
Waterbox
[ ] Construct a functional AGSB
[ ] Get product links given product name
[ ] Logging function
[ ] Multiple browser support
[ ] Multiple supplier support (Walmart, Bestbuy, Microsoft)
[ ] Send me a text message when successful
'''

# ------ libraries ------
import argparse
import requests
import requests_html
import time

from selenium import webdriver
from selenium.webdriver.support.ui import Select

import config

# ------ G variables ------
VERSION = '0.0.1'
TGTURL = config.TGTURL


# ------ functions --------
def main(*args, **kwargs):
    return None


# ------ main -------
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='AGSB arguments')
    parser.add_argument('--name', required=True,
                        help='Specify product name to find and purchase')
    args = parser.parse_args()
    main(target_product=args.name)


# ------ test realm ------
print(config.NAME)
