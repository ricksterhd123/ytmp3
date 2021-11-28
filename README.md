# Youtube downloader

Simple youtube downloader discord bot and web API

## HTTP Endpoints
- /play/(?v=) => Plays downloaded .mp3 file converted from YouTube

## Setup
```bash
# install
pip install virtualenv [--user]

# create an env
virtualenv venv
virtualenv -p /usr/local/bin/pypy venv # using the pypy distribution

# use the env
source myenv/bin/activate

# install dependencies
pip install -r requirements.txt

cd src/

# run flask
cd web/
export FLASK_APP=main.py
# development:
flask run
# production: read gunicorn docs

# run bot
cd bot
python main.py
```
