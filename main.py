from flask import Flask, render_template, request
import listuniversities

listuniversities.init()
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

@app.route('/list_universities')
def list_universities():
    return listuniversities.handle_list_universities()

@app.route('/events')
def events():
    return render_template('events.html')

if __name__ == '__main__':
    app.run('localhost', 1234)
