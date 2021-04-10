from flask import Flask, render_template
from threading import Thread
import os

app = Flask(__name__)
app.secret_key = str(os.environ['secret'])
app.config['SESSION_TYPE'] = 'filesystem'


@app.route('/')
def home():
    return render_template("code.html")

@app.route('/commands')
def commands():
    return render_template("commands.html")

def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()
