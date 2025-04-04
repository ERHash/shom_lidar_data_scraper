# Liste des répertoire disponible ici :
# https://services.data.shom.fr/INSPIRE/telechargement/prepackageGroup?request=GetCapabilities

# Structure des url (exemple):
# https://services.data.shom.fr/YourAPI/telechargement/prepackageGroup/LITTO3D_REUNION_2016_PACK_DL/prepackage/0345_7655/file/0345_7655.7z

import os
import requests
import json

# Clé API 
API_KEY = "YourAPI"
# Répertoire des données (exemple)
DATA_DIRECTORY = "LITTO3D_REUNION_2016_PACK_DL"

# URL de base de l'API
BASE_URL = f"https://services.data.shom.fr/{API_KEY}/telechargement/prepackageGroup/{DATA_DIRECTORY}/"

# En-têtes HTTP à inclure dans les requêtes
headers = {
    'Referer': 'https://diffusion.shom.fr/',  # Ajuster si nécessaire
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',  # User-Agent simulant un navigateur
}

# Fonction pour récupérer le fichier JSON
def get_json_file(url):
    """Récupère le fichier JSON contenant les ressources"""
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print(f"Accès réussi à {url}")
        return response.json()  # Retourne directement un objet Python (dictionnaire)
    else:
        print(f"Erreur d'accès à {url}, statut : {response.status_code}")
        return None

# Nettoyage des données JSON (si nécessaire)
def clean_json(json_data):
    """Simplifie les données JSON en réduisant le tableau des metadataIds à une seule valeur"""
    for resource in json_data.get("prepackageResources", []):
        resource["metadataIds"] = resource["metadataIds"][0]  # Simplifie le tableau des metadataIds à une seule valeur
    return json_data

# Fonction pour extraire les données nécessaires du JSON
def parse_prepackage_json(json_data):
    """Parse les données JSON et extrait les noms des pré-packages et leurs metadataIds"""
    prepackage_data = []
    for prepackage in json_data.get('prepackageResources', []):
        prepackage_name = prepackage['prepackageName']
        metadata_id = prepackage['metadataIds']
        prepackage_data.append({
            'prepackage_name': prepackage_name,
            'metadata_id': metadata_id
        })
    return prepackage_data

# Fonction pour construire le lien de téléchargement des fichiers .7z à partir du pré-package
def build_download_link(prepackage_name, metadata_id):
    """Construit l'URL de téléchargement du fichier .7z en utilisant le nom du pré-package"""
    # On suppose que le fichier .7z est formé de la même manière que le pré-package (ex : 0350_7690.7z)
    # Utilisation du nom de pré-package pour générer l'URL
    download_url = BASE_URL + f"prepackage/{prepackage_name}/file/{prepackage_name}.7z"
    return download_url

# Fonction pour télécharger un fichier .7z avec logs améliorés
def download_file(file_url, file_name):
    """Télécharge le fichier .7z et l'enregistre localement"""
    print(f"Essai de téléchargement de {file_name} depuis {file_url}")
    
    response = requests.get(file_url, headers=headers)
    
    # Afficher les détails de la réponse
    print(f"Statut de la réponse: {response.status_code}")
    print(f"En-têtes de la réponse: {response.headers}")
    
    # Si la réponse est un succès (200 OK)
    if response.status_code == 200:
        print(f"Téléchargement de {file_name} réussi.")
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print(f"{file_name} sauvegardé.")
    else:
        print(f"Erreur lors du téléchargement de {file_name}, statut : {response.status_code}")
        print(f"Contenu de la réponse: {response.text}")  # Afficher les détails du message d'erreur

# Récupérer le fichier JSON
json_url = BASE_URL  # URL vers le fichier JSON des ressources
json_data = get_json_file(json_url)

# Si le fichier JSON a été récupéré avec succès
if json_data:
    # Nettoyer et préparer les données JSON
    cleaned_json_data = clean_json(json_data)
    
    # Analyser les pré-packages extraits du JSON
    prepackage_data = parse_prepackage_json(cleaned_json_data)
    
    # Pour chaque pré-package, construire l'URL de téléchargement et télécharger le fichier .7z
    for prepackage in prepackage_data:
        prepackage_name = prepackage['prepackage_name']
        metadata_id = prepackage['metadata_id']
        
        # Construire l'URL de téléchargement
        download_url = build_download_link(prepackage_name, metadata_id)
        print(f"URL de téléchargement : {download_url}")
        
        # Télécharger le fichier
        file_name = download_url.split("/")[-1]
        download_file(download_url, file_name)
