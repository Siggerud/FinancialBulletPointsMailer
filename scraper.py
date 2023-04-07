import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession

class Scraper:
    def __init__(self, url):
        self._url = url

    def get_json(self):
        response = requests.get(self._url).json()
        response.raise_for_status()

        return response

    def get_soup(self, dynamic=False):
        if not dynamic:
            response = requests.get(self._url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
        else:
            session = HTMLSession()
            response = session.get(self._url)
            response.html.render()
            soup = BeautifulSoup(response.html.raw_html, "html.parser")

        return soup





