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

revival_trance_commander = ['https://gamesempire.com.au/collections/magic-the-gathering/products/magic-the-gathering-final-fantasy-commander-deck-revival-trance',
                            'https://www.pokebox.com.au/products/magic-the-gathering-final-fantasy-revival-trance-red-white-black-commander-deck', 'https://www.deckedoutgaming.com/magic-final-fantasy-commander-deck-revival-trance',
                            'https://www.irresistibleforce.com.au/products/magic-final-fantasy-commander-deck-revival-trance', 'https://www.hobbykitz.com.au/products/pre-order-final-fantasy-commander-deck-revival-trance',
                            'https://shop.tabletopwarfare.com.au/products/magic-the-gathering-final-fantasy-commander-decks-revival-trance', 'https://awgames.com.au/products/final-fantasy-commander-deck-revival-trance-final-fantasy-vi',
                            'https://pastimeparadise.com.au/shop/trading-cards/magic-the-gathering-trading-cards/final-fantasy-commander-deck-revival-trance/', 'https://mayhemcollectables.com.au/products/preorder-magic-final-fantasy-commander-deck-revival-trance']

final_fantasy_booster_box = ['https://awgames.com.au/collections/mtg-sealed-all/products/final-fantasy-play-booster-display', 'https://www.cherrycollectables.com.au/products/magic-the-gathering-final-fantasy-play-booster-box-pre-order-13-jun?from_autocomplete=final+fantasy-7754383982646',
                             'https://www.deckedoutgaming.com/final-fantasy-play-booster-box',
                             'https://shop.goodgames.com.au/products/magic-the-gathering-final-fantasy-play-booster-box?variant=51845426479468', 'https://www.hobbykitz.com.au/products/pre-ordermagic-final-fantasy-bundle?_pos=16&_sid=f672c0a6b&_ss=r',
                             'https://www.irresistibleforce.com.au/products/magic-final-fantasy-play-booster-display?_pos=2&_sid=d31134073&_ss=r','https://www.m-g.com.au/product/mtg-final-fantasy-play-booster-box/',
                             'https://mayhemcollectables.com.au/products/modern-horizons-3-commander-deck-collectors-edition-creative-energy-copy?_pos=6&_sid=53aa9d04b&_ss=r','https://www.pokebox.com.au/products/magic-the-gathering-final-fantasy-play-booster-display',
                             'https://shop.tabletopwarfare.com.au/products/magic-the-gathering-final-fantasy-play-booster-display','https://roningames.com.au/collections/mtg-pre-orders/products/final-fantasy-play-booster-display',
                             'https://popculturelarrikin.com/products/magic-final-fantasy-play-booster-box?_pos=4&_sid=fa1a8f1ad&_ss=r','https://www.gameology.com.au/products/magic-final-fantasy-play-booster-box']

final_fantasy_booster_pack = ['https://www.cherrycollectables.com.au/products/magic-the-gathering-final-fantasy-play-booster-pack-pre-order-13-jun', 'https://www.deckedoutgaming.com/final-fantasy-play-booster',
                              'https://shop.goodgames.com.au/products/magic-the-gathering-final-fantasy-play-booster?variant=51845425791340','https://www.m-g.com.au/product/mtg-final-fantasy-play-booster-single/',
                              'https://www.pokebox.com.au/products/magic-the-gathering-final-fantasy-play-booster-pack','https://popculturelarrikin.com/products/magic-final-fantasy-play-booster?_pos=3&_sid=fa1a8f1ad&_ss=r']

duskmourn_nightmare_bundle = ['https://www.m-g.com.au/product/mtg-duskmourn-house-of-horror-nightmare-bundle/','https://www.cherrycollectables.com.au/products/magic-the-gathering-duskmourn-gift-bundle-box',
                              'https://www.deckedoutgaming.com/duskmourn-house-of-horror-nightmare-bundle','https://www.gameology.com.au/products/magic-duskmourn-house-of-horror-nightmare-bundle',
                              'https://gamesempire.com.au/products/magic-the-gathering-duskmourn-house-of-horror-nightmare-bundle?_pos=5&_sid=f32173b3f&_ss=r','https://pastimeparadise.com.au/shop/trading-cards/duskmourn-house-of-horror-nightmare-bundle/',
                              'https://plentyofgames.com.au/products/duskmourn-house-of-horror-nightmare-bundle?_pos=1&_psq=duskmourn+nightmare+bun&_ss=e&_v=1.0','https://popculturelarrikin.com/products/magic-duskmourn-house-of-horror-nightmare-bundle?_pos=1&_psq=duskmourn+nightmare&_ss=e&_v=1.0',
                              'https://roningames.com.au/collections/trading-card-sealed-product/products/duskmourn-house-of-horror-nightmare-bundle?_pos=1&_sid=00e3239a5&_ss=r', 'https://thecombatcompany.com/products/duskmourn-house-of-horror-bundle-pre-order-sep-1?variant=49350630801702&country=AU&currency=AUD&utm_medium=product_sync&utm_source=google&utm_content=sag_organic&utm_campaign=sag_organic',
                              'https://millenniumcomics.com.au/products/magic-the-gathering-duskmourn-nightmare-bundle','https://guf.com.au/collections/duskmourn/products/magic-the-gathering-duskmourn-house-of-horror-nightmare-bundle']

rat_colony_dominaria_list = ['https://awgames.com.au/products/rat-colony-dominaria?_pos=3&_sid=ad750b25a&_ss=r','https://mayhemcollectables.com.au/products/rat-colony-dominaria?_pos=1&_sid=54b489963&_ss=r',
                             'https://plentyofgames.com.au/products/rat-colony-dominaria?_pos=1&_psq=rat+colony&_ss=e&_v=1.0','https://roningames.com.au/products/rat-colony-dominaria?_pos=1&_sid=b8c2d9866&_ss=r',
                             'https://www.mtgmate.com.au/cards/Rat_Colony/DOM/101','https://gamesportal.com.au/products/mtg-rat-colonydominaria?_pos=1&_psq=rat+colony&_ss=e&_v=1.0',
                             'https://www.thegamescube.com/catalog/magic_singles-pioneer-dominaria/rat_colony/533713','https://elementalarcade.com.au/products/rat-colony-dominaria?_pos=1&_sid=e0558c90e&_ss=r',
                             'https://progamers.com.au/products/mtg-rat-colonydominaria?_pos=6&_sid=d951440dd&_ss=r','https://eternalmagic.cc/products/rat-colony-dominaria?_pos=2&_sid=af4a7753e&_ss=r',
                             'https://magiccards.com.au/content/buy/rat-colony-0','https://thatgamestore.com.au/products/rat-colony-dominaria?_pos=2&_sid=98ba6b4e0&_ss=r','https://tcgsingles.com.au/products/mtg-rat-colonydominaria?_pos=1&_sid=610b40130&_ss=r'
                             'https://guf.com.au/products/rat-colony-dominaria?_pos=1&_sid=7ecc4be9e&_ss=r','https://jenesmtg.com.au/products/rat-colony-dominaria-101?_pos=1&_sid=91033804c&_ss=r','https://www.cracking-tcgsingles.com.au/products/rat-colony-dominaria?_pos=2&_sid=6c194c282&_ss=r&variant=40082999247000',
                             'https://www.cardhouse.com.au/products/rat-colony-dominaria','https://fromthedeepgames.com.au/products/mtg-rat-colonydominaria?_pos=3&_sid=bc9837178&_ss=r',
                             'https://rhysticnostalgiagaming.com.au/products/rat-colony-dominaria?_pos=3&_sid=0fa443ca0&_ss=r']

rat_colony_secret_lair_list_01 = ['https://mayhemcollectables.com.au/products/rat-colony-secret-lair-drop-series?_pos=5&_sid=54b489963&_ss=r','https://plentyofgames.com.au/products/rat-colony-secret-lair-drop-series?_pos=4&_psq=rat+colony&_ss=e&_v=1.0',
                                  'https://roningames.com.au/products/rat-colony-secret-lair-drop?_pos=3&_sid=b8c2d9866&_ss=r','https://gamesportal.com.au/products/mtg-rat-colonysecret-lair-drop-series?_pos=3&_psq=rat+colony&_ss=e&_v=1.0',
                                  'https://www.thegamescube.com/catalog/magic_singles-premium_products_ftv_etc-secret_lair/rat_colony__foil/614045', 'https://elementalarcade.com.au/products/rat-colony-secret-lair-drop-series?_pos=6&_sid=e0558c90e&_ss=r',
                                  'https://progamers.com.au/products/mtg-rat-colony-secret-lair-drop-series?_pos=8&_sid=d951440dd&_ss=r','https://eternalmagic.cc/products/rat-colony-secret-lair-drop-series?_pos=4&_sid=af4a7753e&_ss=r',
                                  'https://thatgamestore.com.au/products/rat-colony-secret-lair-drop?_pos=5&_sid=98ba6b4e0&_ss=r','https://guf.com.au/products/mtg-rat-colony-secret-lair-drop-series?_pos=7&_sid=7ecc4be9e&_ss=r',
                                  'https://tcgsingles.com.au/products/mtg-rat-colonysecret-lair-drop-series?_pos=4&_sid=610b40130&_ss=r','https://www.cracking-tcgsingles.com.au/products/rat-colony-secret-lair-drop?_pos=4&_sid=6c194c282&_ss=r&variant=40094044356760',
                                  'https://www.cardhouse.com.au/products/rat-colony-secret-lair-drop-series','https://rhysticnostalgiagaming.com.au/products/rat-colony-secret-lair-drop-series?_pos=6&_sid=0fa443ca0&_ss=r']

www_substring = "www."
shop_substring = "shop."
com_substring = ".com"
cc_substring = ".cc"

def _get_supplier(supplier_url):
    this_supplier_string = ''
    if com_substring in supplier_url:
        this_supplier_string = supplier_url.split('.com')[0]
    if cc_substring in supplier_url:
        this_supplier_string = supplier_url.split('.cc')[0]
    # if au_substring in supplier_url:
    #     this_supplier_string = supplier_url.split('.au')[0]
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
    if this_supplier == "m-g" or this_supplier == "pastimeparadise":
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
    if this_supplier == "plentyofgames" or this_supplier == "awgames" or this_supplier == "roningames" or this_supplier == "gamesportal" \
            or this_supplier == "elementalarcade" or this_supplier == "progamers" or this_supplier == "eternalmagic" or this_supplier == "thatgamestore" \
            or this_supplier == "tcgsingles" or this_supplier == "cardhouse" or this_supplier == "guf" or this_supplier == "fromthedeepgames":
        return this_soup.find('span', itemprop = 'price')
    if this_supplier == "cherrycollectables":
        return this_soup.find('span', class_ = 'money')
    if this_supplier == "pokebox" or this_supplier == "mayhemcollectables" or this_supplier == "rhysticnostalgiagaming":
        return this_soup.find('span', class_ = 'price')
    if this_supplier == "irresistibleforce":
        return this_soup.find('span', class_ = 'price-item price-item-regular')
    if this_supplier == "hobbykitz" or this_supplier == 'thecombatcompany' or this_supplier == 'jenesmtg':
        return this_soup.find('span', class_ = 'price-item price-item--regular')
    if this_supplier == "tabletopwarfare":
        return this_soup.find('span', class_ = 'product-price--original')
    if this_supplier == "popculturelarrikin":
        return this_soup.find('b', class_ = 'price-item price-item--regular') # can merge this into above matching clause
    if this_supplier == "millenniumcomics":
        return this_soup.find_all('span', class_ = 'price price--highlight')
    if this_supplier == "mtgmate":
        return this_soup.find_all('td', class_ = 'price')
    if this_supplier == "thegamescube":
        return this_soup.find('span', class_ = 'regular price')
    if this_supplier == "magiccards":
        return this_soup.find('span', class_ = 'price-amount')
    if this_supplier == "cracking-tcgsingles":
        return this_soup.find('span', class_ = 'transcy-money')
    else:
        print("Supplier not found! Tried the supplier: ", this_supplier)

def _remove_tags(text):
    clean = re.compile('<.*?>')
    cleaned_text = re.sub(clean, '', text)  # Remove HTML tags
    cleaned_text = cleaned_text.replace('[', '')
    cleaned_text = cleaned_text.replace(']', '')
    cleaned_text = cleaned_text.replace(',', '')
    cleaned_text = cleaned_text.replace('AUD', '')  # Remove 'AUD'
    cleaned_text = cleaned_text.replace('$', '')    # Remove dollar sign
    cleaned_text = cleaned_text.replace('Sale price', '') # Remove 'Sale price'
    cleaned_text = cleaned_text.strip()             # Strip whitespace
    print('Sale price: ', cleaned_text)
    return cleaned_text.strip()

def _write_to_db(product_name, supplier_name, product_url, supplier_price):
    connect = sqlite3.connect('mtg-database.db')
    with sqlite3.connect('mtg-database.db') as prices:
        cursor = prices.cursor()
        cursor.execute('''
                       INSERT INTO CARDPRICES (product_type, supplier, supplier_url, price, lowest_price)
                       VALUES (?, ?, ?, ?, ?) ON CONFLICT(product_type, supplier)
            DO
                       UPDATE SET
                           price = excluded.price,
                           lowest_price = CASE
                           WHEN excluded.price < CARDPRICES.lowest_price OR CARDPRICES.lowest_price IS NULL
                           THEN excluded.price
                           ELSE CARDPRICES.lowest_price
                       END
                       ''', (product_name, supplier_name, product_url, supplier_price, supplier_price))

        prices.commit()
    connect.close()

# Murders at Karlov Play Booster Box
if __name__ == "__main__":
    # Establish db connection, create table if not there
    connect = sqlite3.connect('mtg-database.db')
    connect.execute('CREATE TABLE IF NOT EXISTS CARDPRICES (product_type TEXT, supplier TEXT, supplier_url TEXT, price REAL, lowest_price REAL, UNIQUE(product_type, supplier))')
    connect.close()

    for product_url in revival_trance_commander:
        product_name = 'commander-deck-revival-trance'
        supplier_name = _get_supplier(product_url)
        supplier_price = _scrape_site(product_url, supplier_name)
        _write_to_db(product_name, supplier_name, product_url, supplier_price)

    for product_url in final_fantasy_booster_box:
        product_name = 'final-fantasy-play-booster-box'
        supplier_name = _get_supplier(product_url)
        supplier_price = _scrape_site(product_url, supplier_name)
        _write_to_db(product_name, supplier_name, product_url, supplier_price)

    for product_url in final_fantasy_booster_pack:
        product_name = 'final-fantasy-play-booster'
        supplier_name = _get_supplier(product_url)
        supplier_price = _scrape_site(product_url, supplier_name)
        _write_to_db(product_name, supplier_name, product_url, supplier_price)

    for product_url in duskmourn_nightmare_bundle:
        product_name = 'duskmourn-house-of-horror-nightmare-bundle'
        supplier_name = _get_supplier(product_url)
        supplier_price = _scrape_site(product_url, supplier_name)
        _write_to_db(product_name, supplier_name, product_url, supplier_price)

    for product_url in rat_colony_dominaria_list:
        product_name = 'rat-colony-dominaria'
        supplier_name = _get_supplier(product_url)
        supplier_price = _scrape_site(product_url, supplier_name)
        _write_to_db(product_name, supplier_name, product_url, supplier_price)

    for product_url in rat_colony_secret_lair_list_01:
        product_name = 'rat-colony-secret-lair-drop'
        supplier_name = _get_supplier(product_url)
        supplier_price = _scrape_site(product_url, supplier_name)
        _write_to_db(product_name, supplier_name, product_url, supplier_price)

    # To scrape:
    # https://www.gamesworldsa.com.au/collections/magic-the-gathering
    # https://tcg.tabernaclegames.com.au/collections/sealed-mtg?page=4
    # https://www.emeraldhobbies.com.au/collections/magic-the-gathering
    # https://www.thegamescorner.com.au/products/magic-the-gathering-final-fantasy-commander-deck-revival-trance-release-date-13-jun-2025?variant=49633373159710
    # https://popculturelarrikin.com/products/magic-final-fantasy-play-booster?variant=50165573255462&country=AU&currency=AUD&utm_medium=product_sync&utm_source=google&utm_content=sag_organic&utm_campaign=sag_organic&gad_source=1&gad_campaignid=21016189429&gclid=EAIaIQobChMIiLrhkvWajQMVQcdMAh00owPUEAQYAyABEgK2VPD_BwE

    # TODO:
    # Method that checks for sold out

    # Missing sites:
    # EB games - has anti botting using required cookies/javascript
    # Gamesmen - behind cloudflare. Knows Im a bot
    # gamezknight has emojis in their class names and i cbf with it