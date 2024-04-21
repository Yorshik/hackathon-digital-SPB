import requests

params_for_geocode = {"geocode": "пр. Кузнецова 22к1", "lang": "ru_RU", "format": "json"}

response = requests.get("https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b", params=params_for_geocode).json()

coords = response["response"]["GeoObjectCollection"]['featureMember'][0]['GeoObject']["Point"]