import requests
from bs4 import BeautifulSoup
import os

def save_resource(url, save_path):
    response = requests.get(url, stream=True)
    with open(save_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

def scrape_site(url, output_dir):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for link in soup.find_all('link', rel='stylesheet'):
        href = link['href']
        if not href.startswith('http'):
            href = url + '/' + href
        file_name = os.path.basename(href)
        save_resource(href, os.path.join(output_dir, file_name))

    for script in soup.find_all('script', src=True):
        src = script['src']
        if not src.startswith('http'):
            src = url + '/' + src
        file_name = os.path.basename(src)
        save_resource(src, os.path.join(output_dir, file_name))

    with open(os.path.join(output_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(soup.prettify())



scrape_site(url, output_dir)
