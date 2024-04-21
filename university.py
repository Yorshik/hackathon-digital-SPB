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

def handle_university():
    direction = request.args.get('direction')
    ege = request.args.get('ege')
    direction_name = ""
    vuzes = []
    if ege and direction:
        nap = find_direction(direction)
        direction_name = nap.name
        vuzes = university_parser.get_universities_by_direction(nap, 10)
    return render_template('university.html',
                           vuzes=vuzes, direction=direction_name)


