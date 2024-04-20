from pprint import pprint

from test_schedule import get_schedule


def from_unix_time(timestamp):
    min, sec = timestamp // 60, timestamp % 60
    hour, min = min // 60, min % 60
    return hour, min, sec


def make_schedule():
    schedule = get_schedule()
    for day in ['ПОНЕДЕЛЬНИК', 'ВТОРНИК', 'СРЕДА', 'ЧЕТВЕРГ', 'ПЯТНИЦА', 'СУББОТА', 'ВОСКРЕСЕНЬЕ']:
        lessons = schedule[day]
        print(day)
        breaks = []
        if lessons:
            for i in range(len(lessons) - 1):
                breaks.append((from_unix_time(lessons[i]["time"][1]), from_unix_time(lessons[i + 1]["time"][0] - lessons[i]["time"][1])))
            lessons_start = from_unix_time(lessons[0]["time"][0])
            lessons_end = from_unix_time(lessons[-1]["time"][1])
            pprint(breaks)
            print(lessons_start, lessons_end)
        print()


if __name__ == "__main__":
    make_schedule()
