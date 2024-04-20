from flask import Flask, render_template, request
import university_parser

directions = None
def init():
    directions = get_directions()

def find_direction(string):
    d = None
    for item in directions:
        if item.code == string:
            d = item
            break
    return d

def handle_list_universities():
    direction = request.form.get('direction')
    ege = request.form.get('ege')
    nap = find_direction(direction)
    vuzes = get_universities_by_direction(nap, 10)
    return render_template('listuniversities.html',
                           vuzes=vuzes, direction=nap.name)



