from flask import Flask, render_template, request
from test_api import get_events

import requests

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/apartments')
def apartments():
    return render_template('apartments.html')


@app.route('/schedule')
def schedule():
    return render_template('schedule.html')

@app.route('/university')
def university():
    return render_template('university.html')

@app.route('/events')
def events():
    address = request.form.get("address")
    print(address)
    events = []
    if address is not None:
        events = get_events(["Развлечения"])
    
    return render_template('events.html', list_of_events=events)

if __name__ == '__main__':
    app.run('localhost', 1234)
