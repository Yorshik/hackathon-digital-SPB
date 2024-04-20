import json
from pprint import pprint

import requests


def get_schedule(group_number=2181):
    url = "https://digital.etu.ru/api/mobile/schedule"
    params = {
        "groupNumber": group_number
    }

    page = requests.get(url, params=params)
    result_json = json.loads(page.text)["2181"]["days"]
    all_days = {}
    for day in result_json.values():
        schedule = []
        repetitions = []
        for lesson in day["lessons"]:
            if lesson["start_time"] in repetitions:
                continue
            else:
                repetitions.append(lesson["start_time"])
            lesson = {
                "title": lesson["name"],
                "time": (lesson["start_time_seconds"], lesson["end_time_seconds"]),
                "housing": lesson["room"][0] if lesson["room"] else None
            }
            schedule.append(lesson)
        all_days[day["name"]] = schedule
    return all_days


if __name__ == "__main__":
    pprint(get_schedule())
