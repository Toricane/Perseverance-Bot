from flask import Flask, render_template, request
from threading import Thread
import os

app = Flask(__name__)
app.secret_key = str(os.environ['secret'])
app.config['SESSION_TYPE'] = 'filesystem'


@app.route('/')
def home():
    agent = request.headers.get('User-Agent')
    phones = ["iphone", "android", "blackberry"]
    if any(phone in agent.lower() for phone in phones):
        return render_template('home_mobile.html')
    else:
        return render_template("home_desktop.html")

@app.route('/commands')
def commands():
    agent = request.headers.get('User-Agent')
    phones = ["iphone", "android", "blackberry"]
    if any(phone in agent.lower() for phone in phones):
        return render_template('commands_mobile.html')
    else:
        return render_template("commands_desktop.html")

def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()
