import json
from pprint import pprint

import requests


def get_cafes(address_coordinates, count_results):
    yandex_org_apikey = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'
    yandex_org = 'https://search-maps.yandex.ru/v1/'
    lat, lng = address_coordinates
    params = {
            'apikey': yandex_org_apikey,
            'text': 'кафе',
            'lang': 'ru_RU',
            'll': f'{lng},{lat}'
    }
    req = requests.get(yandex_org, params=params)
    if not req:
        print(req.status_code, req.reason)
        print(req.url)
    js = req.json()
    js = js["features"]

    two_gis_key = "13b57cb5-57b2-4d8d-bd6e-aace69d00c8e"
    url = f"https://routing.api.2gis.com/get_dist_matrix?key={two_gis_key}&version=2.0"
    result = []
    for i in range(count_results):
        coords = js[i]["geometry"]["coordinates"]

        headers = {
            'Content-Type': 'application/json',
        }

        params = {
            'key': two_gis_key,
            'version': '2.0',
        }

        json_data = {
            'points': [
                {'lat': 59.971868,
                    'lon': 30.323690},
                {'lat': coords[1],
                    'lon': coords[0]}],
            'sources': [0],
            'targets': [1],
        }

        response = requests.post('https://routing.api.2gis.com/get_dist_matrix', params=params, headers=headers,
                                 json=json_data)

        duration = response.json()["routes"][0]["duration"]

        data = js[i]["properties"]["CompanyMetaData"]

        cafe = (data["name"], data["address"], duration)
        result.append(cafe)
    return result


if __name__ == "__main__":
    pprint(get_cafes((59.971868, 30.323690), 3))