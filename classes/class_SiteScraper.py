from abc import ABC, abstractmethod

class SiteScraper(ABC):
    @abstractmethod
    def __init__(self, link):
        pass

    @abstractmethod
    def scraper(self):
        pass