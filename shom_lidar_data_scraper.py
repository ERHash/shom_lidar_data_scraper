import os
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

# Clé API 
API_KEY = "YourAPIkey"
# Répertoire des données (exemple)
DATA_DIRECTORY = "L3D_LIDAR_POLYNESIE_BOR_2015_PACK_DL"

# Liste des répertoire disponible ici :
# https://services.data.shom.fr/INSPIRE/telechargement/prepackageGroup?request=GetCapabilities

# URL de base de l'API
BASE_URL = f"https://services.data.shom.fr/{API_KEY}/telechargement/prepackageGroup/{DATA_DIRECTORY}/"

# Structure des url (exemple):
# https://services.data.shom.fr/YourAPIkey/telechargement/prepackageGroup/LITTO3D_BZH_2018_2021_PACK_DL/prepackage/0275_6855/file/0275_6855.7z

# En-têtes HTTP à inclure dans les requêtes
headers = {
    'Authorization': f'Bearer {API_KEY}',  # Si nécessaire pour l'authentification
    'Referer': 'https://services.data.shom.fr',  # Ajustez si nécessaire en fonction de l'API /!\
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',  # User-Agent simulant un navigateur
}

# Fonction pour récupérer le fichier XML
def get_xml_file(url):
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print(f"Accès réussi à {url}")
        return response.content
    else:
        print(f"Erreur d'accès à {url}, statut : {response.status_code}")
        return None

# Fonction pour parser le XML et extraire les informations sur les prepackage
def parse_prepackage_xml(xml_content):
    # Utilisation d'ElementTree pour parser le XML
    root = ET.fromstring(xml_content)
    
    prepackage_data = []
    
    # Itérer sur tous les éléments <prepackageResources>
    for prepackage in root.findall('prepackageResources'):
        prepackage_name = prepackage.find('prepackageName').text
        metadata_ids = prepackage.find('metadataIds').text
        
        # Ajouter l'information sur le prepackage et son fichier XML associé
        prepackage_data.append({
            'prepackage_name': prepackage_name,
            'metadata_id': metadata_ids
        })
    
    return prepackage_data

# Fonction pour construire le lien de téléchargement des fichiers .7z à partir du pré-package
def build_download_link(prepackage_name, metadata_id):
    # Lien de base pour télécharger le fichier .7z
    download_url = BASE_URL + f"prepackage/{prepackage_name}/file/{metadata_id.replace('.xml', '.7z')}"
    return download_url

# Fonction pour télécharger un fichier .7z
def download_file(file_url, file_name):
    response = requests.get(file_url, headers=headers)
    
    if response.status_code == 200:
        print(f"Téléchargement de {file_name} réussi.")
        # Sauvegarder le fichier dans le répertoire local
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print(f"{file_name} sauvegardé.")
    else:
        print(f"Erreur lors du téléchargement de {file_name}, statut : {response.status_code}")

# Récupérer le fichier XML
xml_url = url_directory + "fichier_prepackage.xml"  # Remplacer par le vrai nom du fichier XML
xml_content = get_xml_file(xml_url)

if xml_content:
    # Parser le fichier XML pour extraire les pré-packages
    prepackage_data = parse_prepackage_xml(xml_content)
    
    # Pour chaque prepackage, générer les liens de téléchargement et télécharger les fichiers .7z
    for prepackage in prepackage_data:
        prepackage_name = prepackage['prepackage_name']
        metadata_id = prepackage['metadata_id']
        
        # Construire le lien pour télécharger le fichier .7z
        download_url = build_download_link(prepackage_name, metadata_id)
        
        # Télécharger le fichier
        file_name = download_url.split("/")[-1]
        download_file(download_url, file_name)
