import requests
from bs4 import BeautifulSoup  
from queue import Queue
import lxml

START_URL = "https://www.nyu.edu/" 
DOMAIN = "nyu.edu"
  
queue = Queue()
scraped = set()  

def scrape():
    queue.put(START_URL)

    while not queue.empty():
        url = queue.get()
        
        if url in scraped:
            continue
            
        scraped.add(url)
            
        print(f"Scraping: {url}")
      
        try:
            response = requests.get(url)
        except: 
            continue 

        soup = BeautifulSoup(response.content, 'lxml')
        content = soup.find('div', {'class': 'content'}).text 

        links = soup.find_all('a')
        for link in links: 
            href = link.get("href")  
            if href and DOMAIN in href:
                queue.put(href)

scrape()