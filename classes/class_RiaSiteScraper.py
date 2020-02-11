from bs4 import BeautifulSoup as bs
import requests
import lxml
from classes.class_SiteScraper import SiteScraper

class RiaSiteScraper(SiteScraper):

    def __init__(self, link):
        self.site_link = link
        self.name = "Ria"

    def scraper(self):
        html = requests.get(self.site_link)
        soup = bs(html.content, "lxml")
        self.title = []
        self.link = []
        self.text = []

        for element in soup.select(".list-item"):
            content = element.select(".list-item__content > a")
            self.title.append(content[1].text)
            self.link.append(content[1].attrs["href"])
            html_article = requests.get(content[1].attrs["href"])
            soup_article = bs(html_article.content, "lxml")
            self.text.append(soup_article.find('div', {"class": "article__text"}).text)