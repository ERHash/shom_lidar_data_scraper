# Shom Lidar Data Scraper

## Description

Ce projet permet de télécharger des fichiers `.7z` contenant des données Lidar à partir de l'API du SHOM (Service Hydrographique et Océanographique de la Marine) en utilisant une clé API. Le script récupère les informations des pré-packages via un fichier JSON et télécharge ensuite les fichiers associés dans un répertoire local spécifié.

Les données sont utilisées pour des applications telles que la cartographie et l'analyse des fonds marins, en particulier dans le cadre du projet LITTO3D.

## Prérequis

- Python 3.6 ou supérieur
- Les modules Python suivants :
  - `requests`
  - `json`
  - `os`

Installer ces modules via pip :

```bash
pip install requests
```

## Utilisation

1. Cloner ce dépôt ou télécharger le fichier `shom_lidar_data_scraper.py`.

```bash
git clone https://github.com/ton-utilisateur/shom-lidar-data-scraper.git
cd shom-lidar-data-scraper
```

2. Modifier la clé API / Jeton et le répertoire de données si nécessaire.

Ouvrir le fichier `shom_lidar_data_scraper.py` et vérifier que la clé API / Jeton et le répertoire des données sont correctement définis.

```python
# Clé API
API_KEY = "YourAPI"
# Répertoire des données
DATA_DIRECTORY = "LITTO3D_REUNION_2016_PACK_DL"
```

3. Exécute le script pour télécharger les fichiers `.7z`.

```bash
python shom_lidar_data_scraper.py
```

Le script téléchargera les fichiers `.7z` dans un répertoire `downloads` créé automatiquement dans le même répertoire que le script.

## Fonctionnalités

- **Récupération des données JSON** : Le script récupère les données des pré-packages en appelant l'API du SHOM.
- **Téléchargement automatique** : Pour chaque pré-package, le script construit une URL de téléchargement et récupère le fichier `.7z` associé.
- **Gestion des erreurs** : Si un fichier n'est pas trouvé (erreur 404), le script affiche un message d'erreur avec les détails du fichier.

## Exemple de sortie

Lors de l'exécution du script, voici ce que tu peux voir dans la console :

```
Accès réussi à https://services.data.shom.fr/YourAPI/telechargement/prepackageGroup/LITTO3D_REUNION_2016_PACK_DL/
URL de téléchargement : https://services.data.shom.fr/YourAPI/telechargement/prepackageGroup/LITTO3D_REUNION_2016_PACK_DL/prepackage/0350_7690/file/0350_7690.7z
Essai de téléchargement de 0350_7690.7z depuis https://services.data.shom.fr/YourAPI/telechargement/prepackageGroup/LITTO3D_REUNION_2016_PACK_DL/prepackage/0350_7690/file/0350_7690.7z
Statut de la réponse: 200
0350_7690.7z sauvegardé dans downloads/.
```

## Structure des fichiers

```
/LITTO3D_REUNION_2016_PACK_DL/
  - shom_lidar_data_scraper.py   # Le script principal
  - downloads/                   # Dossier où les fichiers .7z seront téléchargés
```

## Remerciements

SHOM pour le partage et la mise en ligne des données.

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus d'informations.
```
