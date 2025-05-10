from os import remove

import requests
import re
import random
from bs4 import BeautifulSoup
import sqlite3

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
]

headers = {
    'User-Agent': random.choice(user_agents), 'Upgrade-Insecure-Requests': str(1), 'Accept': 'text/html,application/xhtml+xml,application/xml',
    'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-US,en;q=0.5', 'Connection': 'close'
}

karlov_booster_box = ['https://www.m-g.com.au/product/mtg-murders-at-karlov-manor-play-booster-box/', 'https://vaultgames.com.au/products/murders-at-karlov-manor-play-booster-box?_pos=3&_sid=19ac284bf&_ss=r','https://theboardgamer.com.au/products/magic-the-gathering-murders-at-karlov-manor-play-booster-box-38428933',
                      'https://gamesempire.com.au/products/magic-murders-at-karlov-manor-play-booster-box?_pos=9&_sid=1d0248fdd&_ss=r', 'https://shop.goodgames.com.au/products/magic-the-gathering-murders-at-karlov-manor-play-booster-box-preorder?variant=43011077734558', 'https://www.gameology.com.au/products/magic-murders-at-karlov-manor-play-booster-box',
                      'https://www.deckedoutgaming.com/murders-at-karlov-manor-play-booster-box', 'https://www.plentyofgames.com.au/collections/mtg-sealed/products/murders-at-karlov-manor-play-booster-display']

www_substring = "www."
shop_substring = "shop."

def _get_supplier(supplier_url):
    this_supplier_string = supplier_url.split('.com')[0]
    this_supplier_string = this_supplier_string.split('https://')[1]
    if www_substring in this_supplier_string:
        this_supplier_string = this_supplier_string.split('www.')[1]
    if shop_substring in this_supplier_string:
        this_supplier_string = this_supplier_string.split('shop.')[1]
    return this_supplier_string

def _scrape_site(url, this_supplier):
    this_request = requests.get(url, headers=headers)
    soup = BeautifulSoup(this_request.content, 'html.parser')
    # Find the html tag containing the price which is exclusive to each storefront
    raw_price = _get_price(soup, this_supplier)
    string_price = str(raw_price)
    cleaned_price = _remove_tags(string_price)
    return cleaned_price

def _get_price(this_soup, this_supplier):
    if this_supplier == "m-g":
        return this_soup.find('bdi')
    if this_supplier == "vaultgames":
        return this_soup.find('span', id = 'ProductPrice')
    if this_supplier == "theboardgamer":
        return this_soup.find('span', class_ = 'current-price theme-money')
    if this_supplier == "gamesempire":
        return this_soup.find('span', class_ = 'money')
    if this_supplier == "goodgames":
        return this_soup.find_all('span', class_ = 'money')
    if this_supplier == "gameology":
        return this_soup.find('span', class_ = 'price single--price')
    if this_supplier == "deckedoutgaming":
        return this_soup.find('div', class_ = 'productprice productpricetext')
    if this_supplier == "plentyofgames":
        return this_soup.find('span', itemprop = 'price')
    else:
        return

def _remove_tags(text):
    # Remove HTML tags
    clean = re.compile('<.*?>')
    # return re.sub(clean, '', text)
    cleaned_text = re.sub(clean, '', text)
    # Remove square brackets and commas if we call find_all()
    cleaned_text = re.sub(r'[\[\],$]', '',  cleaned_text)
    # Remove empty space
    return cleaned_text.strip()

# Murders at Karlov Play Booster Box
if __name__ == "__main__":
    # Establish db connection, create table if not there
    connect = sqlite3.connect('mtg-database.db')
    connect.execute('CREATE TABLE IF NOT EXISTS CARDPRICES (product_type TEXT, supplier TEXT, price REAL, UNIQUE(product_type, supplier))')

    for product_url in karlov_booster_box:
        product_name = 'murders-at-karlov-manor-play-booster-box'
        supplier_name = _get_supplier(product_url)
        supplier_price = _scrape_site(product_url, supplier_name)

        with sqlite3.connect('mtg-database.db') as prices:
            cursor = prices.cursor()
            cursor.execute('''
                           INSERT INTO CARDPRICES (product_type, supplier, price)
                           VALUES (?, ?, ?) ON CONFLICT(product_type, supplier)
                        DO
                           UPDATE SET price=excluded.price
                           ''', (product_name, supplier_name, supplier_price))
            prices.commit()


    # https://www.ebgames.com.au/search?q=murders+at+karlov
    # https://www.plentyofgames.com.au/collections/mtg-sealed?page=2
    # https://www.cherrycollectables.com.au/pages/search-results?q=murders+at+karlov
    # https://www.gamesworldsa.com.au/collections/magic-the-gathering
    
    # https://webautomation.io/blog/how-to-create-price-comparison-tool-with-beautiful-soup/

    # TODO:
    # Method that checks for sold out
    # Strip $ from retrieved price
