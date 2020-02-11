from bs4 import BeautifulSoup as bs
import requests
from classes.class_SiteScraper import SiteScraper

class TvrSiteScraper(SiteScraper):

    def __init__(self, link):
        self.site_link = link
        self.name = "Tvr"

    def scraper(self):
        self.title = []
        self.link = []
        self.text = []
        html = requests.get(self.site_link)
        soup = bs(html.content, "html.parser")
        for element in soup.select(".text"):
            title = element.select(".title >a")
            self.link.append(self.site_link + title[0].attrs["href"])
            title = title[0].text
            title = title.strip()
            self.title.append(title)
            text = element.find("p").text
            self.text.append(text)