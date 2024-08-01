import unittest
from scraper import WikipediaScraper


class TestWikipediaScraper(unittest.TestCase):

    def test_fetch_page_content(self):
        url = "https://en.wikipedia.org/wiki/List_of_animal_names"
        scraper = WikipediaScraper(url)
        content = scraper.fetch_page_content()
        self.assertIn("<html", content)

    def test_parse_html(self):
        html_content = "<html><body><table class='wikitable'><tr><th>Header</th></tr></table></body></html>"
        tables = WikipediaScraper.parse_html(html_content)
        self.assertEqual(len(tables), 1)


if __name__ == '__main__':
    unittest.main()
