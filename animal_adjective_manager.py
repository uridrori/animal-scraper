from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import re
from scraper import WikipediaScraper


class AnimalAdjectiveManager:
    def __init__(self):
        self.animal_adjectives = defaultdict(list)

    def parse_table(self, html_content):
        table = WikipediaScraper.parse_html(html_content)[0]
        headers = [header.text.strip() for header in table.find('tr').find_all('th')]

        animal_col = headers.index('Scientific term') if 'Scientific term' in headers else headers.index('Animal')
        trivial_col = headers.index('Trivial name') if 'Trivial name' in headers else None
        adjective_col = headers.index('Collateral adjective')

        # Use a ThreadPoolExecutor for concurrent processing of rows
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for row in table.find_all('tr')[1:]:  # Skip header row
                columns = row.find_all('td')
                if len(columns) > max(animal_col, adjective_col):
                    future = executor.submit(self._process_row, columns, animal_col, trivial_col, adjective_col)
                    futures.append(future)

            # Ensure all threads complete
            for future in futures:
                future.result()

    def _process_row(self, columns, animal_col, trivial_col, adjective_col):
        animal = columns[animal_col].text.strip()
        if trivial_col is not None:
            animal += f" ({columns[trivial_col].text.strip()})"
        adjectives = columns[adjective_col].text.strip().split(',')

        # Clean up each adjective
        cleaned_adjectives = [self._clean_text(adj) for adj in adjectives]

        self._add_animal_adjectives(animal, cleaned_adjectives)

    def _clean_text(self, text):
        # Use regex to retain only alphabetic characters and spaces
        cleaned_text = re.sub(r'[^a-zA-Z\s]', '', text)
        return cleaned_text.strip()

    def _add_animal_adjectives(self, animal, adjectives, img_path=None):
        for adj in adjectives:
            adj = adj.strip()
            if adj:
                self.animal_adjectives[adj].append((animal, img_path))

    def output_to_html(self, filename):
        with open(filename, 'w') as f:
            f.write('<html><body>')
            for adjective, animals in self.animal_adjectives.items():
                f.write(f'<h2>{adjective}</h2>')
                f.write('<ul>')
                for animal, img_path in animals:
                    if img_path:
                        f.write(f'<li>{animal} <img src="{img_path}" alt="{animal}" width="100"></li>')
                    else:
                        f.write(f'<li>{animal}</li>')
                f.write('</ul>')
            f.write('</body></html>')