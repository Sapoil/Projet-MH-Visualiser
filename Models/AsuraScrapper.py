from Scrapper.ManhuaScrapper import ManhuaScrapper
from Utils.Utils import get_html_elements, download_image

class AsuraScrapper(ManhuaScrapper):

    def __init__(self, url):
        super().__init__(url)
        

    def getTitle(self):
        return " ".join(self.url.split("/")[4].split("-")[0:-1]).title()

    def chapterUrlEnd(self):
        return "/chapter/"
    
    # def getChapters(self):
    #     stoppers = self.getStopper()
    #     for i in range(stoppers[0], stoppers[1] + 1):
    #         chapter = self.Chapter(self,self.url + "/chapter/", i, self.path)
    #         self.chapters.append(chapter)

    def getCover(self):
        elements = get_html_elements(self.url, 'img')
        for element in elements:
            if element.get('alt') == ['poster']:
                image_url = element['src']
                image_name = "cover.jpg"
                download_image(image_url, self.path, image_name)
                return  self.path + "/" + image_name
        
    def getStopper(self):
        elements = get_html_elements(self.url, 'span')
        begin, end = -1, -1
        for element in elements:
            if element.get('class') == ['pl-[1px]']:
                if begin == -1:
                    begin = int(element.text)
                else:
                    end = int(element.text)
        return begin, end
    
    def imgFilter(self, image):
        return (not image.get('src').startswith('/images'))