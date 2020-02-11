from flask import Flask, jsonify
from classes.class_SiteScraperFactory import SiteScraperFactory

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
