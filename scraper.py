import requests
from bs4 import BeautifulSoup


class WikipediaScraper:
    def __init__(self, url):
        self.url = url

    def fetch_page_content(self):
        response = requests.get(self.url)
        return response.text

    @staticmethod
    def parse_html(html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup.find_all('table', {'class': 'wikitable'})
