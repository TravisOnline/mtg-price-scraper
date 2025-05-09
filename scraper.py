from os import remove

import requests
import re
import random
from bs4 import BeautifulSoup

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
]

headers = {
    'User-Agent': random.choice(user_agents), 'Upgrade-Insecure-Requests': str(1), 'Accept': 'text/html,application/xhtml+xml,application/xml',
    'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-US,en;q=0.5', 'Connection': 'close'
}

def remove_tags(text):
    # Remove HTML tags
    clean = re.compile('<.*?>')
    # return re.sub(clean, '', text)
    cleaned_text = re.sub(clean, '', text)
    # Remove square brackets and commas if we call find_all()
    cleaned_text = re.sub(r'[\[\],]', '',  cleaned_text)
    # Remove empty space
    return cleaned_text.strip()

# Murders ar Karlov Play Booster Box
if __name__ == "__main__":
    # Mind Games Online
    mgo = requests.get('https://www.m-g.com.au/product/mtg-murders-at-karlov-manor-play-booster-box/', headers=headers)
    soup = BeautifulSoup(mgo.content, 'html.parser')
    raw_price = soup.find('bdi')
    string_price = str(raw_price)
    actual_price = remove_tags(string_price)
    print('Mind Games Online: ', actual_price)

    # Vault Games
    vg = requests.get('https://vaultgames.com.au/products/murders-at-karlov-manor-play-booster-box?_pos=3&_sid=19ac284bf&_ss=r', headers=headers)
    soup = BeautifulSoup(vg.content, 'html.parser')
    raw_price = soup.find('span', id = 'ProductPrice')
    string_price = str(raw_price)
    actual_price = remove_tags(string_price)
    print('Vault Games: ', actual_price)

    # The Board Gamer
    bg = requests.get('https://theboardgamer.com.au/products/magic-the-gathering-murders-at-karlov-manor-play-booster-box-38428933', headers=headers)
    soup = BeautifulSoup(bg.content, 'html.parser')
    raw_price = soup.find('span', class_ = 'current-price theme-money')
    string_price = str(raw_price)
    actual_price = remove_tags(string_price)
    print('The Board Gamer: ', actual_price)

    # Games Empire
    ge = requests.get('https://gamesempire.com.au/products/magic-murders-at-karlov-manor-play-booster-box?_pos=9&_sid=1d0248fdd&_ss=r')
    soup = BeautifulSoup(ge.content, 'html.parser')
    raw_price = soup.find('span', class_ = 'money')
    string_price = str(raw_price)
    actual_price = remove_tags(string_price)
    print('Games Empire: ', actual_price)

    # Good Games Shop
    gg = requests.get('https://shop.goodgames.com.au/products/magic-the-gathering-murders-at-karlov-manor-play-booster-box-preorder?variant=43011077734558')
    soup = BeautifulSoup(gg.content, 'html.parser')
    raw_price = soup.find_all('span', class_ = 'money')
    string_price = str(raw_price)
    actual_price = remove_tags(string_price)
    print('Good Games Shop: ', actual_price)

    # Gameology
    gameology = requests.get('https://www.gameology.com.au/products/magic-murders-at-karlov-manor-play-booster-box')
    soup = BeautifulSoup(gameology.content, 'html.parser')
    raw_price = soup.find('span', class_ = 'price single--price')
    string_price = str(raw_price)
    actual_price = remove_tags(string_price)
    print('Gameology: ', actual_price)

    # Decked out gaming
    do = requests.get('https://www.deckedoutgaming.com/murders-at-karlov-manor-play-booster-box')
    soup = BeautifulSoup(do.content, 'html.parser')
    raw_price = soup.find('div', class_ = 'productprice productpricetext')
    string_price = str(raw_price)
    actual_price = remove_tags(string_price)
    print('Decked Out Gaming: ', actual_price)

    # Plenty of games
    pog = requests.get('https://www.plentyofgames.com.au/collections/mtg-sealed/products/murders-at-karlov-manor-play-booster-display')
    soup = BeautifulSoup(pog.content, 'html.parser')
    raw_price = soup.find('span', itemprop = 'price')
    string_price = str(raw_price)
    actual_price = remove_tags(string_price)
    print('Plenty of games: ', actual_price)

    # https://www.ebgames.com.au/search?q=murders+at+karlov
    # https://www.plentyofgames.com.au/collections/mtg-sealed?page=2
    # https://www.cherrycollectables.com.au/pages/search-results?q=murders+at+karlov
    # https://www.gamesworldsa.com.au/collections/magic-the-gathering
    
    # https://webautomation.io/blog/how-to-create-price-comparison-tool-with-beautiful-soup/

    # TODO:
    # Method that checks for sold out
