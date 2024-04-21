from flask import Flask, render_template, request
import university
from events_api import get_events
from get_new_buildings import *

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


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
    return render_template('schedule.html')

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
