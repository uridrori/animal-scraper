from collections import defaultdict
import threading
from scraper import WikipediaScraper
from image_downloader import ImageDownloader
import os


class AnimalAdjectiveManager:
    def __init__(self):
        self.animal_adjectives = defaultdict(list)

    def parse_table(self, html_content):
        table = WikipediaScraper.parse_html(html_content)
        image_download_threads = []

        headers = [header.text.strip() for header in table.find('tr').find_all('th')]

        animal_col = headers.index('Scientific term') if 'Scientific term' in headers else headers.index('Animal')
        trivial_col = headers.index('Trivial name') if 'Trivial name' in headers else None
        adjective_col = headers.index('Collateral adjective')

        for row in table.find_all('tr')[1:]:  # Skip header row
            columns = row.find_all('td')
            if len(columns) > max(animal_col, adjective_col):
                animal = columns[animal_col].text.strip()
                if trivial_col is not None:
                    animal += f" ({columns[trivial_col].text.strip()})"
                adjectives = columns[adjective_col].text.strip().split(',')

                img_tag = columns[animal_col].find('img')
                img_url = ImageDownloader.get_image_url(img_tag) if img_tag else None

                if img_url:
                    thread = threading.Thread(target=self._download_and_add_image, args=(img_url, animal, adjectives))
                    image_download_threads.append(thread)
                    thread.start()
                else:
                    self._add_animal_adjectives(animal, adjectives)

        for thread in image_download_threads:
            thread.join()

    def _download_and_add_image(self, img_url, animal, adjectives):
        img_path = ImageDownloader.download_image(img_url, animal)
        self._add_animal_adjectives(animal, adjectives, img_path)

    def _add_animal_adjectives(self, animal, adjectives, img_path=None):
        for adj in adjectives:
            adj = adj.strip()
            if adj:
                self.animal_adjectives[adj].append((animal, img_path))

    def output_to_html(self, filename):
        with open(filename, 'w') as f:
            f.write('<html><body>')
            for adjective, animals in self.animal_adjectives.items():
                f.write(f'<h2>Collateral adjective: {adjective}</h2>')
                f.write('<ul>')
                for animal, img_path in animals:
                    if img_path:
                        f.write(f'<li>{animal} <img src="{img_path}" alt="{animal}" width="100"></li>')
                    else:
                        f.write(f'<li>{animal}</li>')
                f.write('</ul>')
            f.write('</body></html>')