"""
from terminal:
set FLASK_APP=app.py
set FLASK_ENV=development
set FLASK_DEBUG=1
flask run
"""

from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "index"

@app.route("/buy")
def buy():
    return 'buy'

@app.route("/sell")
def sell():
    return "sell"

@app.route("/setting2")
def settings():
    return "settings"