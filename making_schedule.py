from datetime import datetime
from pprint import pprint

from get_schedule import get_schedule
from get_cafes import get_cafes


def to_str_time(time):
    return f"{time[0]}:{time[1]}"


def from_unix_time(timestamp):
    min, sec = timestamp // 60, timestamp % 60
    hour, min = min // 60, min % 60
    return hour, min, sec


def make_schedule(group_name, day=None):
    if day is None:
        day = str(datetime.weekday(datetime.now()))
    else:
        day = str(day)
    lessons, day_name = get_schedule(day, group_name)

    times = []
    schedule = []
    if lessons:
        cafes = get_cafes((59.971868, 30.323690), len(lessons) - 1)
        for i in range(len(lessons)):
            times.append((i + 1, from_unix_time(lessons[i]["time"][0]),
                          from_unix_time(lessons[i]["time"][1])))

            start = to_str_time(from_unix_time(lessons[i]["time"][0]))
            end = to_str_time(from_unix_time(lessons[i]["time"][1]))
            housing = lessons[i]['housing'] if lessons[i]['housing'] else "не определён"
            periods = {
                "num": i + 1,
                "name": lessons[i]["title"],
                "time": f"{start}-{end}",
                "address": f"ЛЭТИ, корпус {housing}"
            }
            schedule.append(periods)

            if i < len(lessons) - 1:
                time_for_walk = cafes[i][-1]
                times.append((None, from_unix_time(lessons[i]["time"][1] + time_for_walk),
                              from_unix_time(lessons[i + 1]["time"][0] - time_for_walk)))

                start = to_str_time(from_unix_time(lessons[i]["time"][1] + time_for_walk))
                end = to_str_time(from_unix_time(lessons[i + 1]["time"][0] - time_for_walk))
                housing = cafes[i][1]
                periods = {
                    "num": None,
                    "name": cafes[i][0],
                    "time": f"{start}-{end}",
                    "address": housing
                }

                schedule.append(periods)

        for time in times:
            pass

    else:
        pass
    result = {"day": day_name,
              "events": schedule}
    pprint(result)
    return result


if __name__ == "__main__":
    make_schedule("2181")
