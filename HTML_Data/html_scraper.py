import requests
from bs4 import BeautifulSoup
import os
from queue import Queue
import lxml

# Allowed domain
DOMAIN = "nyu.edu"  

# Folder to save text files
folder = "scraped_texts"
os.mkdir(folder)  

def scrape(url):
    try:
        res = requests.get(url)  
    except Exception as e:
        print(e)
        return 

    soup = BeautifulSoup(res.text, 'lxml')
    
    # Logic to extract text 
    text = ""
    for p in soup.find_all('p'):
        text += p.text + "\n"

    # Get clean file name
    name = url.replace("/", "_")

    # Save text file  
    file_path = os.path.join(folder, name + ".txt")
    with open(file_path, "w") as f:
        f.write(text)

    links = soup.find_all('a')
        
    urls = []
    for a in links:
        href = a.get("href") 
        if href and DOMAIN in href:
            urls.append(href)
    
    return urls

# Initialize    
start_url = "https://www.nyu.edu/"
queue = Queue()
queue.put(start_url)  

processed = set()   

while not queue.empty():
    url = queue.get()  
    if url in processed:
        continue

    processed.add(url)  
    links = scrape(url)
    
    for link in links:
        queue.put(link)
        
print("Scrape complete")