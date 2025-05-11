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

if __name__ == "__main__":
    store_url = 'https://gamesempire.com.au/collections/magic-the-gathering/products/magic-the-gathering-final-fantasy-commander-deck-revival-trance'
    this_request = requests.get(store_url, headers=headers)
    soup = BeautifulSoup(this_request.content, 'html.parser')
    # print(soup)
    # Find the html tag containing the price which is exclusive to each storefront
    raw_price = soup.find_all('span', class_ = 'money')
    # print("Raw price: ",raw_price)
    if raw_price:
        string_price = str(raw_price)
        clean = re.compile('<.*?>')
        cleaned_text = re.sub(clean, '', string_price)  # Remove HTML tags
        cleaned_text = cleaned_text.replace('[', '')
        cleaned_text = cleaned_text.replace(']', '')
        cleaned_text = cleaned_text.replace(',', '')
        cleaned_text = cleaned_text.replace('AUD', '')  # Remove 'AUD'
        cleaned_text = cleaned_text.replace('$', '')    # Remove dollar sign
        cleaned_text = cleaned_text.replace('Sale price', '') # Remove sale price
        cleaned_text = cleaned_text.strip()             # Strip whitespace
        print("Price is:", cleaned_text)