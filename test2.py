import requests
from bs4 import BeautifulSoup
import os

def save_resource(url, save_path):
    # Télécharge la ressource et l'enregistre dans le fichier spécifié
    response = requests.get(url, stream=True)
    with open(save_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

def scrape_site(url, output_dir):
    # Récupère le contenu de l'URL et le parse avec BeautifulSoup
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Crée le répertoire de sortie s'il n'existe pas
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Enregistre les fichiers CSS référencés dans les balises <link>
    for link in soup.find_all('link', rel='stylesheet'):
        href = link['href']
        if not href.startswith('http'):
            href = url + '/' + href
        file_name = os.path.basename(href)
        save_resource(href, os.path.join(output_dir, file_name))

    # Enregistre les fichiers JavaScript référencés dans les balises <script>
    for script in soup.find_all('script', src=True):
        src = script['src']
        if not src.startswith('http'):
            src = url + '/' + src
        file_name = os.path.basename(src)
        save_resource(src, os.path.join(output_dir, file_name))

    # Enregistre le fichier HTML
    with open(os.path.join(output_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

url = 'https://www.example.com'  # Remplacez ceci par l'URL du site Web que vous souhaitez scraper
output_dir = 'output'  # Remplacez ceci par le répertoire de sortie souhaité

scrape_site(url, output_dir)
