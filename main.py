from flask import Flask, render_template, request
import university
from test_api import get_events

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
