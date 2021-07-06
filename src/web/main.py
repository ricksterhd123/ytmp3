from __future__ import unicode_literals
from flask import Flask
from flask import request
from flask.helpers import send_from_directory
from pathlib import Path
import json

def get_config(file_name):
    """
    Reads file and returns deserialized json
    :params str file_name: file path of config file
    :returns json 
    """
    p = Path(file_name)
    if p.exists():
        with p.open() as f:
            return json.loads(f.read())
    return False


CONFIG_FILE_PATH = "../config.json"
CONFIG = get_config(CONFIG_FILE_PATH)
assert(CONFIG)

app = Flask(__name__)

@app.route('/play/<name>')
def play(name):
    print(name)
    return send_from_directory("../"+CONFIG["filepath"], "{0}.mp3".format(name))

@app.route("/")
def index():
    return "<h1>Welcome to exile's youtube downloader</h1>"
