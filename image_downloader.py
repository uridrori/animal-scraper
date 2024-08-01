import requests
from urllib.parse import urljoin


class ImageDownloader:
    @staticmethod
    def download_image(url, animal_name):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                file_name = f"/tmp/{animal_name.replace(' ', '_')}.jpg"
                with open(file_name, 'wb') as f:
                    f.write(response.content)
                return file_name
        except Exception as e:
            print(f"Error downloading image for {animal_name}: {e}")
        return None

    @staticmethod
    def get_image_url(img_tag):
        if img_tag and 'src' in img_tag.attrs:
            return urljoin('https://en.wikipedia.org', img_tag['src'])
        return None
