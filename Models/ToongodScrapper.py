from Scrapper.ManhuaScrapper import ManhuaScrapper
from Utils.Utils import download_image, get_html_elements


class ToongodScrapper(ManhuaScrapper):
    def __init__(self, url):
        super().__init__(url)
        
    def getTitle(self):
        return " ".join(self.url.split("/")[4].split("-")[0:-1]).title()

    def getChapters(self):
        stoppers = self.getStopper()
        for i in range(stoppers[0], stoppers[1] + 1):
            chapter = self.Chapter(self,self.url + "/chapter-", i, self.path)

    def getCover(self):
        elements = get_html_elements(self.url, 'img')
        for element in elements:
            if element.get('alt') == [self.title.replace(" ", "-")]:
                image_url = element['src']
                image_name = "cover.jpg"
                download_image(image_url, self.path, image_name)
                return  self.path + "/" + image_name
        
    def getStopper(self):
        elements = get_html_elements(self.url, 'li')
        for element in elements:
            if 'Chapter' in element.text:
                chapter_number = int(element.text.split()[-1])
                return (1, chapter_number)
        return (1, 1)
    
    def imgFilter(self, image):
        return (not image.get('src').startswith('/images'))