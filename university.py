from flask import Flask, render_template, request
import university_parser

directions = None
def init():
    global directions
    directions = university_parser.get_directions()

def find_direction(string):
    d = None
    for item in directions:
        if item.code == string:
            d = item
            break
    return d

def filter_vuzes(vuzes, ege):
    return [vuz for vuz in vuzes if ege >= vuz.pass_score]

def handle_university():
    error = None
    direction = request.args.get('direction')
    ege = request.args.get('ege')
    direction_name = ""
    vuzes = []
    try:
        ege = int(ege)
        if ege and direction:
            nap = find_direction(direction)
            if nap is None:
                error = "направление не найдено"
                raise Exception()
            direction_name = nap.name
            vuzes = university_parser.get_universities_by_direction(nap, 10)
            vuzes = filter_vuzes(vuzes, ege)
    except ValueError:
        error = "неправильно написаны числа"
    except:
        pass
    return render_template('university.html',
           vuzes=vuzes, direction=direction_name, ege=ege,dirnum=direction,
                           error=error)


