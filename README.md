# Youtube downloader

Simple youtube downloader discord bot and web API

## Endpoints
- /download/(?v=) => Downloads video and returns JSON containing static file URL lasting up to 20 minutes before it deletes automatically
- /play/ => TBD

## Setup
```bash
# install
pip install virtualenv [--user]

# create an env
virtualenv myenv
virtualenv -p /usr/local/bin/pypy myenv # using the pypy distribution

# use the env
source myenv/bin/activate

# install dependencies
pip install -r requirements.txt

cd src/

# run flask
export FLASK_APP=main.py
flask run
```
