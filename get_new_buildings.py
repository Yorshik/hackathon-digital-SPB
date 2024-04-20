import requests

link = 'https://new_buildings.gate.petersburg.ru/new_buildings'


def get_new_buildings(limit):
    params = {
        'limit': limit
    }
    req = requests.get(link, params=params)
    if not req:
        return 'Something went wrong'
    out = []
    for dct in req.json():
        out.append(dct['dev_fact_address'])

