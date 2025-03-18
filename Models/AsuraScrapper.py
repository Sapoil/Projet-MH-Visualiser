from Scrapper.ManhuaScrapper import ManhuaScrapper
from Utils.Utils import get_html_elements, download_image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class AsuraScrapper(ManhuaScrapper):

    def __init__(self, url):
        super().__init__(url)
        

    def getTitle(self):
        return " ".join(self.url.split("/")[4].split("-")[0:-1]).title()

    def chapterUrlEnd(self):
        return "/chapter/"

    def getCover(self):
        elements = get_html_elements(self.driver,self.url, 'img')
        for element in elements:
            if 'poster' in element.get_attribute('alt'):
                image_url = element.get_attribute('src')
                image_name = "cover.jpg"
                download_image(image_url, self.path, image_name)
                return  self.path + "/" + image_name
        
    def getStopper(self):
        elements = get_html_elements(self.driver, self.url, 'span')
        begin, end = -1, -1
        for element in elements:
            if 'pl-[1px]' in element.get_attribute('class'):
                if begin == -1:
                    begin = int(element.text)
                else:
                    end = int(element.text)
        return begin, end
    
    def imgFilter(self, image):
        return 'chapter' in image.get_attribute('alt')