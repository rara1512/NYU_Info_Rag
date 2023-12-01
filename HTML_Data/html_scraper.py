import requests
from bs4 import BeautifulSoup
import os
from queue import Queue
import lxml

DOMAIN = "nyu.edu"
folder = "scraped_data"
os.mkdir(folder)

def scrape(url):
    try:
        res = requests.get(url)  
    except Exception as e:
        print(e) 
        return []
    
    soup = BeautifulSoup(res.text, 'lxml')
    
    text = "\n".join([p.text for p in soup.find_all('p')])
    
    name = url.replace("/", "_") 
    filepath = os.path.join(folder, name + ".txt")
    with open(filepath, "w") as f:
        f.write(text)

    links = []
    for a in soup.find_all("a"):
        href = a.get("href")
        
        # Handle scheme-less links 
        if href and "//" in href:
           href = "https:" + href
           
        # Filter by domain  
        if href and DOMAIN in href:
            links.append(href)
            
    return links

start_url = "https://www." + DOMAIN  
queue = Queue()
queue.put(start_url)
scraped = set()

while not queue.empty():
    url = queue.get()   
    if url in scraped:
        continue
        
    scraped.add(url)

    # Handle case of no links returned      
    new_links = scrape(url)
    if new_links is None:
        continue

    for link in new_links: 
        queue.put(link)

print("Scrape complete")