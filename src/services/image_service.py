import random

import requests
import os
import urllib.parse
import urllib.request
import json

from src.config import YANDEX_SERVICE_ACC_ID, YANDEX_SERVICE_ACC_API_KEY
from src.utils.parse_yandex_search_xml import parse_yandex_search_xml


def search_image(query, page=0):
    url = "https://yandex.com/images-xml" + \
          "?folderid=" + YANDEX_SERVICE_ACC_ID + \
          "&apikey=" + YANDEX_SERVICE_ACC_API_KEY + \
          "&text=" + query + \
          "&p=" + str(page) + \
          "&iorient=square" + \
          "&isize=large"

    url = urllib.parse.quote(url, safe=':/?&=')

    response = requests.get(url)

    if response.status_code == 200:
        data = parse_yandex_search_xml(response.text)
        print("Image fetched successfully. Count: " + str(len(data["results"])))
        return data
    else:
        print("Failed to fetch image")
        return None


def get_random_image_url(query):
    rand_index = random.randint(0, 40)
    page = rand_index // 20
    index = rand_index % 20

    if not os.path.exists("data/cache.json"):
        with open("data/cache.json", "w") as cache_file:
            json.dump({}, cache_file)

    with open("data/cache.json", "r+") as cache_file:
        try:
            cache = json.load(cache_file)
        except json.JSONDecodeError:
            cache = {}
            json.dump(cache, cache_file)

        if cache and query in cache:
            if cache[query].get(rand_index):
                img = cache[query][rand_index]["url"]
                return img

        result = search_image(query, page)
        if result is not None:
            for to_cache_index in range(0, len(result["results"])):
                if query not in cache:
                    cache[query] = {}
                real_index = page * 20 + to_cache_index
                cache[query][real_index] = result["results"][to_cache_index]
                js = json.dumps(cache)
                cache_file.seek(0)
                cache_file.write(js)
                cache_file.truncate()

            img = result["results"][index]["url"]
            return img
        else:
            print("Failed to fetch image")
            return None


def download_image(url, folder_path):
    name = url.split("/")[-1]
    name = name.split("?")[0]
    path = os.path.join(folder_path, name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    if not os.path.exists(path):
        urllib.request.urlretrieve(url, path)

    return path
