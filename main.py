from flask import Flask, render_template, request
import university
from events_api import get_events
from get_new_buildings import *
from making_schedule import *
from yan_gpt import *

app = Flask(__name__)


@app.route('/', methods=["get","post"])
def index():
    answer = ""
    ask = ""
    if request.method == "POST":
        ask = request.form.get("text")
        answer = gpt_answer(ask)
    return render_template('index.html', ask=ask, answer=answer)


@app.route('/apartments')
def apartments():
    address = request.args.get("address")
    aparts = []
    error = None
    try:
        if address:
            buildings = get_new_buildings()
            aparts = get_closest_buildings(buildings, address)
    except Exception as e:
        error = "При обработке запроса произошла ошибка"
        print(e)
        pass
    return render_template('apartments.html', error=error, address=address, aparts=aparts)


@app.route('/schedule')
def schedule():
    group_name = request.args.get("group")
    schedule = None
    error = None
    try:
        if group_name:
            schedule = make_schedule(group_name)
    except:
        error = "При обработке произошла ошибка"
        pass
    return render_template('schedule.html', error=error, schedule=schedule)

@app.route('/university')
def list_universities():
    return university.handle_university()

@app.route('/events')
def events():
    address = request.args.get("address")
    events = []
    if address:
        events = get_events(["Развлечения"], address)
    
    return render_template('events.html', list_of_events=events, address=address)

if __name__ == '__main__':
    university.init()
    app.run('localhost', 1234)
