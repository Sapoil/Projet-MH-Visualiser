from Models.AsuraScrapper import AsuraScrapper
from Models.ToongodScrapper import ToongodScrapper

class ScrapperNotSupported(Exception):
    pass

class ScrapperFactory:

    @staticmethod
    def getScrapper(url : str):
        if "asura" in url:
            return AsuraScrapper(url)
        else:
            raise ScrapperNotSupported("Scrapper not supported at the moment")