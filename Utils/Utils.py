import os
import requests
from selenium.webdriver.common.by import By
import time

def get_html_elements(driver,page_url, element):
    """Récupère les liens des images d'une page avec JavaScript."""
    try:
        driver.get(page_url)
        time.sleep(1)  # Attendre le chargement du JavaScript
        elements = driver.find_elements(By.TAG_NAME, element)
        return elements
    
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des éléments : {e}")
        return []

def download_image(url, folder_path, image_name):
    """Télécharge une image à partir de son URL."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Vérifie si la requête a réussi

        os.makedirs(folder_path, exist_ok=True)  # Création du dossier si nécessaire

        image_path = os.path.join(folder_path, image_name)
        with open(image_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
    
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors du téléchargement de l'image {url} : {e}")
		
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            return True
        else:
            return False
    except OSError:
        print ('Error: Creating directory. ' +  directory)