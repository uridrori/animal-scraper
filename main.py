# TODO: inspect all files
# TODO: add comments and/or docstrings
# TODO: fix baboon issue

from scraper import WikipediaScraper
from animal_adjective_manager import AnimalAdjectiveManager
import os


def main():
    url = "https://en.wikipedia.org/wiki/List_of_animal_names"

    scraper = WikipediaScraper(url)
    html_content = scraper.fetch_page_content()

    manager = AnimalAdjectiveManager()
    tables = WikipediaScraper.parse_html(html_content)
    for table in tables:
        manager.parse_table(str(table))

    # Output results to HTML file
    output_file = 'animal_adjectives.html'
    manager.output_to_html(output_file)
    print(f"Results have been written to {output_file}")


if __name__ == "__main__":
    main()
