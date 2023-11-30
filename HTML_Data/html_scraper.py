import os
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import tldextract

def save_page(url, soup, base_path):
    domain_name = tldextract.extract(url).domain
    parsed_url = urlparse(url)
    filename = os.path.join(base_path, domain_name, parsed_url.path.lstrip("/").replace("/", "_"))

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename + ".txt", 'w', encoding='utf-8') as f:
        f.write(soup.get_text())

def scrape_website(starting_url, base_path):
    stack = [starting_url]

    while stack:
        current_url = stack.pop()

        response = requests.get(current_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            save_page(current_url, soup, base_path)

            links = soup.find_all('a', href=True)

            for link in links:
                absolute_url = urljoin(current_url, link['href'])

                if urlparse(absolute_url).netloc.endswith('nyu.edu'):
                    stack.append(absolute_url)

if __name__ == "__main__":
    starting_url = "https://www.nyu.edu/"
    base_save_path = "NYU Home"

    scrape_website(starting_url, base_save_path)
