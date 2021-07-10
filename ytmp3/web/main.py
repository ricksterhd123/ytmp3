from __future__ import unicode_literals

# sys.path hack so that ..package can be imported properly
# When i find it necessary, I will do this
# https://stackoverflow.com/questions/6323860/sibling-package-imports/50193944#50193944
import sys
sys.path.append("..") # Adds higher directory to python modules path.

from flask import Flask
from flask import request
from flask.helpers import send_from_directory
from config.read import get_config

print(__file__)
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
