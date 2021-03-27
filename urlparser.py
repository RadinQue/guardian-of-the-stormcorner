from PIL import Image
from io import BytesIO
import requests
from soundfilterer import SoundFilterer

soundfilterer = SoundFilterer()


class URLParser:

    supported_url_image_extensions = [".jpg", ".png", "bmp"]

    async def validate_url(self, url):
        return requests.get(url).status_code == 200

    def url_points_to_image(self, url):
        for extension in self.supported_url_image_extensions:
            if extension in url:
                return True
        return False

    def get_image_object_from_url(self, image_url):
        return Image.open(BytesIO(requests.get(image_url).content))

    def save_audio_from_url(self, url):
        r = requests.get(url, allow_redirects=True)
        if ".mp3" in url:
            open('temp.mp3', 'wb').write(r.content)
            soundfilterer.ffmpeg_convert("temp.mp3", "temp.wav")
        else:
            open('temp.wav', 'wb').write(r.content)
