from bs4 import BeautifulSoup as bs
import requests
from classes.class_TutSiteScraper import TutSiteScraper
from classes.class_TvrSiteScraper import TvrSiteScraper
from classes.class_NewsruSiteScraper import NewsruSiteScraper
from classes.class_RiaSiteScraper import RiaSiteScraper
from classes.class_Article import Article


class SiteScraperFactory:

    def scrap_sites(self):
        scr = NewsruSiteScraper("https://www.newsru.com/world")
        scr.scraper()
        self.all_articles = []
        for i in range(0, len(scr.title)):
            self.all_articles.append(Article(scr.name, scr.title[i], scr.link[i], scr.text[i]))
        scr = TutSiteScraper("https://news.tut.by/world")
        scr.scraper()
        for i in range(0, len(scr.title)):
            self.all_articles.append(Article(scr.name, scr.title[i], scr.link[i], scr.text[i]))
        scr = TvrSiteScraper("https://www.tvr.by/news/v_mire/")
        scr.scraper()
        for i in range(0, len(scr.title)):
            self.all_articles.append(Article(scr.name, scr.title[i], scr.link[i], scr.text[i]))
        # С сайта парсится информация, однако долго, поэтому я закоментил данную операцию, если хотите проверить парсинг сайте напишите [GET] запрос /news/Ria
        # Долгий парсинг из-за того, что текст статьи можно взять только перейдя по ссылке статьи
        """scr=RiaSiteScraper("https://ria.ru/world/")
        scr.scraper()
        for i in range(0,len(scr.title)):
            self.all_articles.append(Article(scr.name,scr.title[i],scr.link[i],scr.text[i]))"""

    def scrap_site(self, site_name):
        if site_name == "Newsru":
            newsruscr = NewsruSiteScraper("https://www.newsru.com/world")
            newsruscr.scraper()
            self.site_articles = []
            for i in range(0, len(newsruscr.title)):
                self.site_articles.append(
                    Article(newsruscr.name, newsruscr.title[i], newsruscr.link[i], newsruscr.text[i]))

        if site_name == "Tut":
            tutscr = TutSiteScraper("https://news.tut.by/world")
            tutscr.scraper()
            self.site_articles = []
            for i in range(0, len(tutscr.title)):
                self.site_articles.append(Article(tutscr.name, tutscr.title[i], tutscr.link[i], tutscr.text[i]))

        if site_name == "Tvr":
            tvrscr = TvrSiteScraper("https://www.tvr.by/news/v_mire/")
            tvrscr.scraper()
            self.site_articles = []
            for i in range(0, len(tvrscr.title)):
                self.site_articles.append(Article(tvrscr.name, tvrscr.title[i], tvrscr.link[i], tvrscr.text[i]))

        if site_name == "Ria":
            riascr = RiaSiteScraper("https://ria.ru/world/")
            riascr.scraper()
            self.site_articles = []
            for i in range(0, len(riascr.title)):
                self.site_articles.append(Article(riascr.name, riascr.title[i], riascr.link[i], riascr.text[i]))