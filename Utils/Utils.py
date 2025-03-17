from bs4 import BeautifulSoup
import requests
import os

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
})

def get_html_elements(url, element):
		try:
			response = session.get(url)
			response.raise_for_status()
			soup = BeautifulSoup(response.text, 'html.parser')
			elements = soup.find_all(element)
			return elements
		except requests.exceptions.RequestException as e:
			print(f"Error fetching the URL: {e}")
			return []
		
def download_image(url, folder_path, image_name):
		try:
			response = session.get(url)
			response.raise_for_status()
			with open(os.path.join(folder_path, image_name), 'wb') as file:
				file.write(response.content)
		except requests.exceptions.RequestException as e:
			print(f"Error downloading the image: {e}")
			
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            return True
        else:
            return False
    except OSError:
        print ('Error: Creating directory. ' +  directory)