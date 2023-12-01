import os
import requests
from bs4 import BeautifulSoup

# Allowed domain 
domain = "nyu.edu/"  

# Root folder to save text files
root_dir = "NYU_Home"
os.makedirs(root_dir, exist_ok=True)

def scrape_site(url, domain):
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
    
    # Follow subdomains
    subdomains = [link["href"] for link in links if domain in link["href"]] 
    
    for url in subdomains:
        scrape_site(url, domain)
        
# Start crawl
base_url = "https://www."+domain
scrape_site(base_url, domain)