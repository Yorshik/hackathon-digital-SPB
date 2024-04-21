import json
from pprint import pprint
import requests


def get_schedule(day_num, group_number=2181):
    group_number = str(group_number)
    url = "https://digital.etu.ru/api/mobile/schedule"
    params = {
        "groupNumber": group_number
    }

    page = requests.get(url, params=params)
    result_json = json.loads(page.text)[group_number]["days"]
    day = result_json[day_num]
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

    return schedule, day["name"]


if __name__ == "__main__":
    pprint(get_schedule("0"))
