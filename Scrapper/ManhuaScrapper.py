	#External imports
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

#Project imports
from Utils.Utils import createFolder, get_html_elements, download_image

#Constants
PATH = "MH/"

class ManhuaScrapper(ABC):
	def __init__(self, url):
		
		chrome_options = Options()
		chrome_options.add_argument("--headless=new")  # Exécuter sans affichage
		chrome_options.add_argument("--disable-gpu")
		chrome_options.add_argument("--no-sandbox")
		chrome_options.add_argument("--window-size=1920x1080")
		chrome_options.add_argument("--disable-software-rasterizer")
		chrome_options.add_argument("--ignore-certificate-errors")  # ✅ Ignore les erreurs SSL
		chrome_options.add_argument("--allow-running-insecure-content")  # ✅ Autorise le contenu non sécurisé

		service = Service()

		self.driver = webdriver.Chrome(service=service, options=chrome_options)
		self.url = url
		self.title = self.getTitle()
		self.path = PATH+self.title
		createFolder(self.path)
		self.chapters = []
		self.cover = self.getCover()

	@abstractmethod
	def getTitle(self):
		pass

	@abstractmethod
	def chapterUrlEnd(self):
		pass

	def getChapters(self):
		stoppers = self.getStopper()
		start, end = stoppers[0], stoppers[1]

		if start == -1 or end == -1:
			print("Erreur: Impossible de déterminer les chapitres.")
			return

		num_chapters = end - start + 1
		max_threads = min(5, num_chapters)  # ✅ Évite d’ouvrir trop de threads

		for i in range(start, end + 1):
			self.download_chapter(i)
			print(f"{int(i/num_chapters*100)}%")

	@abstractmethod
	def getCover(self):
		pass

	@abstractmethod
	def getStopper(self):
		pass

	@abstractmethod
	def imgFilter(self, element):
		pass

	def close(self):
		"""Ferme le driver Selenium proprement."""
		if self.driver:
			self.driver.quit()

	def download_chapter(self, chapter_number):
		chapter = self.Chapter(self, self.url + self.chapterUrlEnd(), chapter_number, self.path)
		self.chapters.append(chapter)

	class Chapter:
		def __init__(self,scrapper, url, nbr, path):
			self.nbr = nbr
			self.url = url + str(nbr)
			self.path = path + "/Chapter_" + str(nbr)
			self.scrapper = scrapper
			self.createChapter()

		def __str__(self):
			return f"Chapter {self.nbr}\nURL: {self.url}\nPath: {self.path}"
		
		def createChapter(self):
			images = get_html_elements(self.scrapper.driver,self.url, 'img')
			images = [image for image in images if self.scrapper.imgFilter(image)]
			if not createFolder(self.path):
				images = [image for image in images if not os.path.exists(self.path + "/" + str(images.index(image)) + ".jpg")]
				if len(images) == 0:
					return
				
			max_threads = min(30, len(images))
			with ThreadPoolExecutor(max_workers=max_threads) as executor:
				future_to_image = {
					executor.submit(download_image, image.get_attribute('src'), self.path, f"{index}.jpg"): image
					for index, image in enumerate(images)
				}

				for future in as_completed(future_to_image):
					try:
						future.result()
					except Exception as e:
						print(f"Error downloading image: {e}")