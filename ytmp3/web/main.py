from __future__ import unicode_literals
from flask import Flask
from flask import request
from flask import abort
from flask import safe_join
from flask.helpers import send_from_directory
from config.read import get_config
from pathlib import Path

print(__file__)
CONFIG_FILE_PATH = "config.json"
CONFIG = get_config(CONFIG_FILE_PATH)
assert(CONFIG)

app = Flask(__name__)

@app.route('/<name>')
def play(name):
    print(name)
    return send_from_directory("../"+CONFIG["filepath"], "{0}.mp3".format(name))

@app.route("/")
def index():
    print("test")
    return INDEX

INDEX = """
<!doctype html>
<html>
    <header>
        <title>YTMP3</title>
    </header>
    <body>
        <h1>Welcome, I am exile's youtube downloader!</h1>
        <p>I am still in development, please come back later!</p>
    </body>
</html>
"""
