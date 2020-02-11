from bs4 import BeautifulSoup as bs
import requests
from classes.class_SiteScraper import SiteScraper

class TutSiteScraper(SiteScraper):

    def __init__(self, link):
        self.site_link = link
        self.name = "Tut"

    def scraper(self):
        html = requests.get(self.site_link)
        soup = bs(html.content, "html.parser")
        self.title = []
        self.link = []
        self.text = []

        for block in soup.select(".news-section.m-rubric"):
            for element in block.select(".news-entry.big.annoticed.time.ni"):
                link = element.select(".entry__link")
                title = element.find("span", {"class": "entry-head _title"}).text
                text = element.find("span", {"class": "entry-note"}).text
                self.title.append(title)
                self.link.append(link[0].attrs["href"])
                self.text.append(text)