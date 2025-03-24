import os
import requests

from historias_de_la_memoria.constants import DIR_PATH


def download_picture(url: str, _id: str) -> str:
    filename = f"{DIR_PATH}/{_id}.jpg"
    user_agent = {'User-agent': 'Mozilla/5.0'}
    os.makedirs(DIR_PATH, exist_ok=True)

    request = requests.get(
        url,
        allow_redirects=True,
        headers=user_agent,
        stream=True,
    )
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)
        return filename
    else:
        raise RuntimeWarning(f"It was impossible to download picture with url: {url}")
