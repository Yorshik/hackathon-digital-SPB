import time

import requests
import math

link = 'https://new_buildings.gate.petersburg.ru/new_buildings'
yandex_org_apikey = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'
yandex_org = 'https://search-maps.yandex.ru/v1/'
geocoder_apikey = '40d1649f-0493-4b70-98ba-98533de7710b'
yandex_geocoder = 'https://geocode-maps.yandex.ru/1.x'
opencage_apikey = 'a63f5a2378284cb6817f0f63bdc6ab68'


def get_new_buildings(limit=20):
    """
    Получение новостроек по апи
    :param limit: Максимаьное количество возвращаемых зданий
    :return: список словарей. В каждом словаре имеется 2 ключа: адрес дома и сайт дома?
    """
    params = {
        'limit': limit
    }
    req = requests.get(link, params=params)
    if not req:
        return 'Something went wrong'
    out = []
    for dct in req.json():
        out.append({'address': dct['dev_fact_address'], 'site': dct['dev_site']})
    return out[:limit]


def distance(xy1: tuple[float, float], xy2: tuple[float, float]):
    """
    расстояние между 2мя точками, рассчитывается по формуле расстояния на поверзности сферы
    :param xy1: координаты 1го места (широта долгота)
    :param xy2: координаты 2го места (широта долгота)
    :return: число
    """
    x1, y1 = xy1
    x2, y2 = xy2
    s = math.acos(
        math.sin(math.radians(x1)) * math.sin(math.radians(x2)) + math.cos(math.radians(x1)) * math.cos(
            math.radians(x2)
        ) * math.cos(math.radians(abs(y1 - y2)))
    ) * 6371 * 1000
    return s


def get_coordinates_opencage(addr):
    """
    координаты которые нашел opencage
    :param addr: адрес ввиде строки
    :return: координаты (широта, долгота)
    """
    url = f'https://api.opencagedata.com/geocode/v1/json?q={addr}&key={opencage_apikey}'
    response = requests.get(url)
    data = response.json()
    lat = data['results'][0]['geometry']['lat']
    lng = data['results'][0]['geometry']['lng']
    return lat, lng


def get_coordinates_yandex(addr):
    """
    координаты которые нашел yandex
    :param addr: адрес ввиде строки
    :return: координаты (широта, долгота)
    """
    params = {
        'apikey': geocoder_apikey,
        'format': 'json',
        'geocode': addr
    }
    req = requests.get(yandex_geocoder, params=params)
    data = req.json()
    try:
        toponym = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
        lng, lat = map(float, toponym['Point']['pos'].split())
        return lat, lng
    except IndexError:
        return None, None


def get_coordinates(addr):
    """
    поиск координат. Если opencage нашел что-то - это возвращается, если нет - возвращается то что нашел яндекс. Если и яндекс ничего не нашел - возвращется None, None
    :param addr: адрес ввиде строки
    :return: координаты (широта, долгота) или None, None
    """
    try:
        lat, lng = get_coordinates_opencage(addr)
    except IndexError:
        lat, lng = get_coordinates_yandex(addr)
    return lat, lng


def get_closest_buildings(buildings, center, limit=10):
    """
    Поиск ближайших зданий
    если функция get_coordinates() вернула None, None то это здание пропускается
    :param buildings: список словарей который возвращает get_buildings
    :param center: адрес места ввиде строик. Будет считаться расстояние от такого-то здания до этого места
    :param limit: сколько возвращать зданий (максимум)
    :return: списко словарей. В каждом словаре имеется 4 ключа: координаты (широта, долгота), address (адрес здания ввиде строки), site (сайт здания?) и distance (расстояние от здания до center)
    """
    center_coordinates = get_coordinates(center)
    out = []
    for building in buildings:
        building_coordninates = get_coordinates(building['address'])
        if not (building_coordninates[0] and building_coordninates[1]):
            continue
        dct = {
            'name': building['address'],
            'distance': distance(center_coordinates, building_coordninates),
            'site': building['site'],
            'coordinates': building_coordninates
        }
        print(dct)
        out.append(dct)
    print('-' * 13)
    out.sort(key=lambda d: d['distance'])
    return out[:limit]


if __name__ == '__main__':
    t1 = time.time()
    print(*get_closest_buildings(get_new_buildings(), 'СПбГЭТУ ЛЭТИ'), sep='\n')
    t2 = time.time()
    print(t2 - t1)
