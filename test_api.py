import datetime
import json
import pprint

import requests


def from_unix_date(timestamp):
    value = datetime.datetime.fromtimestamp(timestamp)
    return value.strftime('%Y-%m-%d %H:%M:%S')


def from_unix_time(timestamp):
    min, sec = timestamp // 60, timestamp % 60
    hour, min = min // 60, min % 60
    return hour, min, sec

CATEGORY_SLUG = {'Активный отдых': 'recreation',
                 'Акции и скидки': 'stock',
                 'Благотворительность': 'social-activity',
                 'Вечеринки': 'party',
                 'Выставки': 'exhibition',
                 'Детям': 'kids',
                 'Квесты': 'quest',
                 'Кинопоказы': 'cinema',
                 'Концерты': 'concert',
                 'Мода и стиль': 'fashion',
                 'Обучение': 'education',
                 'Праздники': 'holiday',
                 'Развлечения': 'entertainment',
                 'Разное': 'other',
                 'События для бизнеса': 'business-events',
                 'Спектакли': 'theater',
                 'Фестивали': 'festival',
                 'Фотография': 'photo',
                 'Шопинг (Магазины)': 'shopping',
                 'Экскурсии': 'tour',
                 'Ярмарки (Развлечения, Ярмарки)': 'yarmarki-razvlecheniya-yarmarki'}


def get_events(input_categories, address):
    categories = ",".join([CATEGORY_SLUG[category] for category in input_categories])
    radius = 2
    APIKEY = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJhU1RaZm42bHpTdURYcUttRkg1SzN5UDFhT0FxUkhTNm9OendMUExaTXhFIn0.eyJleHAiOjE4MDgyOTc2MjcsImlhdCI6MTcxMzYwMzIyNywianRpIjoiNzYwYTFjZGItYTQ0Ni00YzAwLWEzYTUtMTMzNzk5MzRkNmQxIiwiaXNzIjoiaHR0cHM6Ly9rYy5wZXRlcnNidXJnLnJ1L3JlYWxtcy9lZ3MtYXBpIiwiYXVkIjoiYWNjb3VudCIsInN1YiI6IjY1OGQzOTI1LTdlODAtNDk3NS05NzM5LTJiMTNhM2E0MzllZCIsInR5cCI6IkJlYXJlciIsImF6cCI6ImFkbWluLXJlc3QtY2xpZW50Iiwic2Vzc2lvbl9zdGF0ZSI6IjI3ODY2MjBjLWQxODAtNGJhZi05NjFlLWM4M2Q2Y2JkMGU0NSIsImFjciI6IjEiLCJhbGxvd2VkLW9yaWdpbnMiOlsiLyoiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbImRlZmF1bHQtcm9sZXMtZWdzLWFwaSIsIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6ImVtYWlsIHByb2ZpbGUiLCJzaWQiOiIyNzg2NjIwYy1kMTgwLTRiYWYtOTYxZS1jODNkNmNiZDBlNDUiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsIm5hbWUiOiJQYXNoY2hua28gQWxleGV5IiwicHJlZmVycmVkX3VzZXJuYW1lIjoiYTJlYzczYWI5NTVhMzE2MTVkNjRhYjMyMzE1NzNiMmIiLCJnaXZlbl9uYW1lIjoiUGFzaGNobmtvIiwiZmFtaWx5X25hbWUiOiJBbGV4ZXkifQ.kLHcH1Dlajt9WmmeDZJu97CEwKrFH658cmXisjyIcMolPMPy74LsgJ-lq5cj3XhqrkSl54knqL9T2YyEHDtbn3aFUjNxUoLSzSeCLe0ZqLwCgIt9IYTFpPMl14yhZVCoHQgmZ5pExzqYCDtv4H1Ry9Bv-yv2vezx8-tRbGwLXqP228nAmWdrs7yaBQpNkW5LXy6a_wZKQxNZRDUYeFiyR4BaZvtjr9xYX6soO7lzgSC165ujq_d_Vto2zJ2NusYuCVFpBDnhL7qinfrIHcC6kX0HXzO43gN-3uRtlJh0SyiK-OvxaS-ZuRAMfHtXMHkk5Xy2f-2RFGHfbrszTTVvRA"
    count = 30
    fields = "id,title,place,dates,price,site_url"

    params_for_geocode = {"geocode": address, "lang": "ru_RU", "format": "json"}

    res = requests.get("https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b", params=params_for_geocode).json()

    coords = res["response"]["GeoObjectCollection"]['featureMember'][0]['GeoObject']["Point"]["pos"].split()
    
    params = {"lat": coords[1],
              "lng": coords[0],
              "radius": radius,
              "fields": fields,
              "count": count,
              "categories": categories,
              "expand": "place",
              "actual_since": datetime.datetime.now().timestamp()}

    url = "https://spb-afisha.gate.petersburg.ru/kg/external/afisha/events"
    page = requests.get(url, params=params)
    print(page.status_code)
    result_json = json.loads(page.text)
    all_events = []
    for input_event in result_json["data"]:
        event = {
            "title": input_event["title"],
            "coords": input_event["place"]["coords"],
            "price": input_event["price"],
            "address": input_event["place"]["address"],
            "subway": input_event["place"]["subway"],
            "date": from_unix_date(input_event["dates"][0]["start"]),
            "url": input_event["place"]["site_url"],
            "duration": from_unix_time(input_event["dates"][0]["start"] - input_event["dates"][0]["end"])
        }
        all_events.append(event)
    return all_events


if __name__ == "__main__":
    get_events(["Развлечения"])
