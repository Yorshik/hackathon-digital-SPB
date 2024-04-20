import requests

# TODO move it somewhere
geocoder_apikey = '40d1649f-0493-4b70-98ba-98533de7710b'
geocoder_link = 'https://geocode-maps.yandex.ru/1.x/'
map_link = 'http://static-maps.yandex.ru/1.x/'
searcher_apikey = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'
searcher = 'https://search-maps.yandex.ru/v1/'

def get_res_with_lowest_score(data: list[str, str, int]):
    data.sort(key=lambda x: x[-1])
    return data[:15]


def get_university_coordinates(name):
    params = {
        'apikey': geocoder_apikey,
        'format': 'json',
        'geocoder': name
    }
    req = requests.get(geocoder_link)
