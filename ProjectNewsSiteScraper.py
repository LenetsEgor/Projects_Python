from bs4 import BeautifulSoup as bs
import requests
from abc import ABC, abstractmethod
import lxml
from flask import Flask, jsonify


class Article:

    def __init__(self, name, title, link, text):
        self.name = name
        self.title = title
        self.link = link
        self.text = text


class SiteScraper(ABC):
    @abstractmethod
    def __init__(self, link):
        pass

    @abstractmethod
    def scraper(self):
        pass


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


app = Flask(__name__)


@app.route("/news")
def get_all_articles():
    newsscraper = SiteScraperFactory()
    newsscraper.scrap_sites()
    articles = []
    for element in newsscraper.all_articles:
        articles.append({"name": element.name, "title": element.title, "link": element.link, "text": element.text})
    return jsonify({"news": articles}), 200


@app.route("/news/<string:site>")
def get_site_article(site: str):
    try:
        newsscraper = SiteScraperFactory()
        newsscraper.scrap_site(site)
        articles = []
        for element in newsscraper.site_articles:
            articles.append({"name": element.name, "title": element.title, "link": element.link, "text": element.text})
        return jsonify({site: articles}), 201
    except:
        return "500 error", 500


@app.errorhandler(500)
def internal_error(error):
    return "500 error", 500


@app.errorhandler(404)
def not_found(error):
    return "404 error", 404


if __name__ == "__main__":
    app.run()
