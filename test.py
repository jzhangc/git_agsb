#!/usr/bin/env python3
"""
command test realm
"""

# ------libraries ------
from requests_html import HTMLSession

# ------ var ------
product_link = 'https://www.bestbuy.ca/en-ca/product/hp-14-laptop-natural-slver-amd-athlon-silver-3050u-256gb-ssd-8gb-ram-windows-10/15371258'

# ------ test ------
r = HTMLSession()
r = r.get(product_link)

# r.html.render(sleep=5, timeout=20)
for item in r.html.xpath('//*[@id="test"]/button'):
    print(item.text)
