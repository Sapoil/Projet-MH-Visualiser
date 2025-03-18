import time
from Factory.ScrapperFactory import ScrapperFactory

#TODO: Prevoir une queue de manhua a telecharger, et eventuellement permettere de telecharger plusieurs manhua en meme temps via des threads
# TODO: Prevoir un systeme de telechargement automatique des nouveaux chapitres
# TODO: Gestion de stockage
# TODO: Faire une interface graphique adaptable pour Android (libraire Kivy et buildozer)
# TODO: Faire un stockage dans une BD SQLite

#Toongod non pris en compte, probablement générer avec JS, donc il faudrait utiliser Selenium
if __name__ == "__main__":
	start = time.time()
	url = "https://asuracomic.net/series/the-regressed-son-of-a-duke-is-an-assassin-5f701ed2"  # Replace with the target URL
	try:
		mh = ScrapperFactory.getScrapper(url)
		mh.getChapters()
	except Exception as e:
		print(e)
	finally:
		mh.close()
		end = time.time()
		print(f"Execution time: {end - start} seconds")
	