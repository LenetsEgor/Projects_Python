from bs4 import BeautifulSoup as bs
import requests
from classes.class_SiteScraper import SiteScraper

class NewsruSiteScraper(SiteScraper):

    def __init__(self, link):
        self.site_link = link
        self.name = "Newsru"

    def scraper(self):
        html = requests.get(self.site_link)
        soup = bs(html.content, "html.parser")
        self.title = []
        self.link = []
        self.text = []

        for element in soup.select(".index-news-item"):
            content = element.find("a", {"class": "index-news-title"})
            self.title.append(content.text.strip())
            self.link.append(self.site_link[0:22] + content.attrs["href"])
            self.text.append(element.find("a", {"class": "index-news-text"}).text.strip())