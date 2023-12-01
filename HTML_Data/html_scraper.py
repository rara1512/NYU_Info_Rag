import os
import requests
import lxml
from bs4 import BeautifulSoup
from queue import Queue

# Allowed domain 
domain = "nyu.edu"  

# Root folder to save text files
root_dir = "scraped_data"
os.makedirs(root_dir, exist_ok=True)

def scrape_site(queue, domain):
    while not queue.empty():
        url = queue.get()
        
        try:
            res = requests.get(url)
        except: 
            return  

        soup = BeautifulSoup(res.text, 'lxml')
        
        # Get text content from paragraph tags
        text = "" 
        for paragraph in soup.find_all('p'):
            text += paragraph.text + "\n"
        
        # Create file based on url 
        file_name = url.replace("https://", "")
        file_name = file_name.replace("/", "_")
        file_path = os.path.join(root_dir, file_name + ".txt")
        
        # Save text content 
        with open(file_path, "w") as f:
            print(url, file=f)  
            f.write(text)
            
        links = soup.find_all('a')
        
        for link in links: 
            href = link.get("href")  
            if href and domain in href:
                queue.put(href)
        
# Start crawl

base_url = "https://www."+domain

queue = Queue()  
queue.put(base_url)

scraped = set()

# Start
sites = 0

while not queue.empty():
    url = queue.get()
    
    if url in scraped:
        continue

    scraped.add(url)
    sites+=1
    print("Site number = ",sites)
    print("Scraping - ",url)

    try:
        res = requests.get(url)
    except: 
        continue  

    soup = BeautifulSoup(res.text, 'lxml')
    
    # Get text content from paragraph tags
    text = "" 
    for paragraph in soup.find_all('p'):
        text += paragraph.text + "\n"
    
    # Create file based on url 
    file_name = url.replace("https://", "")
    file_name = file_name.replace("/", "_")
    file_path = os.path.join(root_dir, file_name + ".txt")
    
    # Save text content 
    with open(file_path, "w") as f:
        print(url, file=f)  
        f.write(text)
        
    links = soup.find_all('a')
    
    for link in links: 
        href = link.get("href")  
        if href and domain in href:
            queue.put(href)
# End