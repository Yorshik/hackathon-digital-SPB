from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')



@app.route('/VUZ')
def VUZ():
    return render_template('VUZ.html')

if __name__ == '__main__':
    app.run('localhost', 1234)