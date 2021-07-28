from __future__ import unicode_literals

<<<<<<< HEAD
# # sys.path hack so that ..package can be imported properly
# # When i find it necessary, I will do this
# # https://stackoverflow.com/questions/6323860/sibling-package-imports/50193944#50193944
# import sys
# sys.path.append("..") # Adds higher directory to python modules path.
=======
# sys.path hack so that ..package can be imported properly
# When i find it necessary, I will do this
# https://stackoverflow.com/questions/6323860/sibling-package-imports/50193944#50193944
import sys
sys.path.append("..") # Adds higher directory to python modules path.
>>>>>>> f834499404c37b31e32e39a53ac978291d3c5530

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

@app.route('/play/<id>')
def play(id):
    filepath = CONFIG["filepath"]
    filename = "{0}.mp3".format(id)
    try:
        p = Path(safe_join(filepath, filename))
    except:
        pass

    if p and p.is_file():
        return send_from_directory(filepath, filename)
    else:
        return abort(404, description="File not found")

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
