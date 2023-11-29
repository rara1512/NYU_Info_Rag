import os
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import tldextract

def save_page(url, content, base_path):
    domain_name = tldextract.extract(url).domain
    parsed_url = urlparse(url)
    filename = os.path.join(base_path, domain_name, parsed_url.path.lstrip("/").replace("/", "_"))

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename + ".txt", 'w', encoding='utf-8') as f:
        f.write(content)

def scrape_website(url, base_path):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        save_page(url, response.text, base_path)

        links = soup.find_all('a', href=True)

        for link in links:
            absolute_url = urljoin(url, link['href'])

            if urlparse(absolute_url).netloc.endswith('nyu.edu'):
                scrape_website(absolute_url, base_path)

if __name__ == "__main__":
    starting_url = "https://www.nyu.edu/"
    base_save_path = "NYU Home Page"

    scrape_website(starting_url, base_save_path)

